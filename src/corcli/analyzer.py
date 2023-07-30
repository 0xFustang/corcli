"""
Module to use analysers
"""
import concurrent.futures

try:
    from corcli.cortex import Cortex
except ModuleNotFoundError:
    from cortex import Cortex

def run_analyzers(parameters) -> None:
    """Submit analyzer jobs using one or more observables

    Args:
        parameters (dict): Parameters for Cortex submission.

    Returns:
        None
    """
    cortex = Cortex(parameters)

    if not parameters.alias:
        print("No alias selected. Going to selector...")
        target_analyzer = cortex.select_analyzers()
    else:
        target_analyzer = parameters.alias
        cortex.authentication()

    print(f"Analysis in progress for {parameters.observable_data} ....")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_sub = {
            executor.submit(
            cortex.run_analyzer_job,
            parameters.observable_data,
            param): param for param in target_analyzer}

        for future in concurrent.futures.as_completed(future_sub):
            param = future_sub[future]
            print("---")
            print(f'Result for analyzer {param}:\n')
            try:
                response = future.result()
                if parameters.extract_only:
                    if not response:
                        response = future.result()
                        print("No observables extracted.\n")
                    else:
                        for line in response:
                            if "size:" in line:
                                print(f"{line}\nInfo: use -df/--download-files to download file.")
                            else:
                                print(line)
                elif parameters.full_report:
                    print(response) # Show the full analysis report in json
                else:
                    if not response:
                        response = future.result()
                        print("No summary report. Use -fr argument to display the full report.\n")
                    elif ("failed" or "deleted") in response:
                        print(response)
                    else:
                        for line in response:
                            print(line)
            except KeyboardInterrupt:
                for future in future_sub:
                    print("Canceling tasks ...")
                    future.cancel()
            except Exception as e:
                print(f'Something went wrong while launching a job for {param}: \n{e}')
            finally:
                executor.shutdown(wait=True)

def run_analyzers_bulk(parameters) -> None:
    """Submit analyzer jobs using one or more observables

    Args:
        parameters (dict): Parameters for Cortex submission.

    Returns:
        None
    """
    cortex = Cortex(parameters)

    if not parameters.alias:
        print("No alias selected. Going to selector...")
        target_analyzer = cortex.select_analyzers()
    else:
        target_analyzer = parameters.alias
        cortex.authentication()

    print(f"Analysis in progress....")

    for observable in parameters.observables_bulk:

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_sub = {executor.submit(cortex.run_analyzer_job, observable, param): param for param in target_analyzer}

            for future in concurrent.futures.as_completed(future_sub):
                param = future_sub[future]
                print("---")
                print(f'{observable} - Result for analyzer {param}:\n')
                try:
                    response = future.result()
                    if parameters.extract_only:
                        if not response:
                            response = future.result()
                            print("No observables extracted.\n")
                        else:
                            for line in response:
                                print(line)
                    elif parameters.full_report:
                        print(response) # Show the full analysis report in json
                    else:
                        if not response:
                            response = future.result()
                            print("No summary report. Use -fr argument to display the full report.\n")
                        else:
                            for line in response:
                                print(line)
                except KeyboardInterrupt:
                    for future in future_sub:
                        print("Canceling tasks ...")
                        future.cancel()
                except Exception as e:
                    print(f'Something went wrong while launching a job for {param}: \n{e}')
                finally:
                    executor.shutdown(wait=True)
