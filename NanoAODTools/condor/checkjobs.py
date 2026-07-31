import subprocess
import re
import os
import sys
import pandas as pd

def get_file_sizes(directory_url, cert_path, ca_path):
    try:
        # Esegui il comando davix-ls per ottenere la lista dei file e le loro dimensioni
        result = subprocess.run([
            'davix-ls', '-l', '-E', cert_path, '--capath', ca_path, directory_url
        ], capture_output=True, text=True, check=True)
        
        # Leggi l'output del comando
        output = result.stdout
        
        # Dichiara un dizionario per contenere i nomi dei file e le loro dimensioni
        file_sizes = {}
        
        # Analizza l'output riga per riga
        for line in output.splitlines():
            # Ignora le righe non relative ai file (come intestazioni o directory)
            if line.endswith('.root') and line:
                parts = line.split()
                # L'ultima parte è il nome del file
                file_name = parts[-1]
                # La quarta parte è la dimensione del file
                file_size = parts[2]
                file_sizes[file_name] = int(file_size)
        
        return file_sizes
    
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione di davix-ls: {e}")
        return {}

def find_folder(redirector, username, remote_dir, dataset_label, cert_path, ca_path):
    results = subprocess.run([
        'davix-ls', '-E', cert_path, '--capath', ca_path, redirector+"/store/user/"+username+"/"+remote_dir+"/"+dataset_label+"/"
    ], capture_output=True, text=True, check=True)
    subfold = results.stdout.splitlines()
    subfold.sort()
    subfold = subfold[-1]

    return redirector+"/store/user/"+username+"/"+remote_dir+"/"+dataset_label+"/"+subfold

def job_exit_code(job_logFile):
    exit_code = None

    with open(job_logFile, "r") as f:
        lines = f.readlines()

    # Search for the last line with "Normal termination"
    for line in reversed(lines):
        match = re.search(r'return value (\d+)\)', line)
        if match:
            exit_code = int(match.group(1))
            break

    # if exit_code is not None:
    #     print(f"Exit code: {exit_code}")
    # else:
    #     print("No exit code found.")

    return exit_code

def checkSubmitStatus(redirector, username, uid, sample, running_folder, remote_folder_name):
    import os
    # print("Sample: ", sample.label)
    listoffile = os.listdir(running_folder+"/"+sample.label)

    # check number of total number of files that should have been created
    jobs_total = 0 
    for f in listoffile: 
        if f.startswith("file"):
            n = int(f.split("file")[-1])
            if n>jobs_total: jobs_total = n
    jobs_total += 1


    # check number of files that have been actually created
    davixfolder                     = find_folder(redirector, username, remote_folder_name, sample.label, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    # print("davixfolder: ", davixfolder)
    file_sizes                      = get_file_sizes(davixfolder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    total_files_onTier              = len(file_sizes)
    fileNumbers_onTier              = [int(file_name.split("_")[-1].split(".")[0]) for file_name, file_size in file_sizes.items()]
    njobs_toResubmit     = 0
    njobs_notFoundOnTier = 0
    njobs_emptyFile      = 0
    jobs_toResubmit_notFoundOnTier = []
    jobs_toResubmit_emptyFile      = []
    for jobNumber in range(jobs_total):
        resubmit_job     = False
        file_name        = f"tree_hadd_{jobNumber}.root"
        if jobNumber not in fileNumbers_onTier:
            # print(f"Job {jobNumber} not found on tier")
            njobs_notFoundOnTier            += 1
            njobs_toResubmit                += 1
            jobs_toResubmit_notFoundOnTier.append(jobNumber)
            resubmit_job                     = True
        else:
            file_size = file_sizes[file_name]
            if file_size < 1000:
                # print(f"File: {file_name}, Size: {file_size} bytes")
                njobs_emptyFile             += 1
                njobs_toResubmit            += 1
                jobs_toResubmit_emptyFile.append(jobNumber)
                resubmit_job                 = True

        if resubmit_job:
            file_num            = str(jobNumber)
            sample_folder       = running_folder+"/"+sample.label+"/file"+file_num+"/"
            # print("Removing empty file from tier...  "+file_name)
            # print("davix-rm "+davixfolder+"/"+file_name+" -E /tmp/x509up_u"+str(uid)+" --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
            # os.popen("davix-rm "+davixfolder+"/"+file_name+" -E /tmp/x509up_u"+str(uid)+" --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
            # print("Resubmitting...")
            # print("condor_submit "+sample_folder+"condor.sub")
            # os.popen("condor_submit "+sample_folder+"/condor.sub")
            # print("\n")

    return jobs_total, total_files_onTier, njobs_toResubmit, njobs_notFoundOnTier, njobs_emptyFile, jobs_toResubmit_notFoundOnTier, jobs_toResubmit_emptyFile


def summarize_job_status(username, uid, samples, running_folder, remote_folder_name):
    summary = []

    for sample in samples:
        try:
            jobs_total, total_on_tier, to_resubmit, not_found, empty, jobs_toResubmit_notFoundOnTier, jobs_toResubmit_emptyFile = checkSubmitStatus(username, uid, sample, running_folder, remote_folder_name)
            summary.append({
                "Sample": sample.label,
                "Jobs Total": jobs_total,
                "Files on Tier": total_on_tier,
                "To Resubmit": to_resubmit,
                "Not Found on Tier": not_found,
                "Empty Files": empty,
                "Jobs Not Found": jobs_toResubmit_notFoundOnTier,
                "Jobs Empty": jobs_toResubmit_emptyFile,
            })
        except Exception as e:
            summary.append({
                "Sample": sample.label,
                "Jobs Total": "ERROR",
                "Files on Tier": "ERROR",
                "To Resubmit": "ERROR",
                "Not Found on Tier": "ERROR",
                "Empty Files": "ERROR",
                "Jobs Not Found": "ERROR",
                "Jobs Empty": "ERROR",
            })
            print(f"Error processing sample {sample.label}: {e}")

    df = pd.DataFrame(summary)
    return df

def check_errors_fromcondor(dataset, username, uid, remote_folder_name, redirector, resubmit=False, delete_files_fromtier=False):
    err_folder = os.environ.get('PWD')+ f"/tmp/{dataset}/condor/error/"
    log_folder = os.environ.get('PWD')+ f"/tmp/{dataset}/condor/log/"
    output_folder = os.environ.get('PWD')+ f"/tmp/{dataset}/condor/output/"
    tmp_folder = os.environ.get('PWD')+ f"/tmp/{dataset}/"
    listoffile = os.listdir(err_folder)
    list_of_job_errors = subprocess.run(f"grep -l '(Davix::HttpRequest) Error' {err_folder}/*.err", shell=True, capture_output=True, text=True)
    jobs_with_errors = list_of_job_errors.stdout.split('\n')
    jobs_with_errors_numbers = [e.split("_")[-1].replace(".err","") for e in jobs_with_errors[:-1]]
    str_resubmit = ""
    for e in jobs_with_errors_numbers:
        str_resubmit += f"condor_submit tmp/{dataset}/{e}/condor.sub; "
    if not resubmit:
        print(f"Found {len(jobs_with_errors_numbers)} jobs with Davix errors in dataset {dataset}. To resubmit them, run:\n{str_resubmit}")
    else:
        print(f"Resubmitting {len(jobs_with_errors_numbers)} jobs with Davix errors in dataset {dataset}...")
        for n in jobs_with_errors_numbers:
            subprocess.run(f"rm {err_folder}/{dataset}_{n}.err", shell=True, capture_output=True, text=True)
            subprocess.run(f"rm {output_folder}/{dataset}_{n}.out", shell=True, capture_output=True, text=True)
            subprocess.run(f"rm {log_folder}/{dataset}_{n}.log", shell=True, capture_output=True, text=True)
        print("REMOVED condor log, err and out files ")
        subprocess.run(str_resubmit, shell=True, capture_output=True, text=True)
    if delete_files_fromtier:
        print(f"Deleting files from tier for {len(jobs_with_errors_numbers)} jobs with Davix errors in dataset {dataset}...")
        jobs_to_delete = [n.replace("file", "") for n in jobs_with_errors_numbers]
        print("Files to be deleted:\n "+str(jobs_to_delete))
        for n in jobs_to_delete:
            davixfolder = find_folder(redirector, username, remote_folder_name, dataset, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
            file_name = f"tree_hadd_{n}.root"
            print(f"davix-rm {davixfolder}/{file_name} -E /tmp/x509up_u{uid} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
            result = subprocess.run(f"davix-rm {davixfolder}/{file_name} -E /tmp/x509up_u{uid} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/", shell=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Error: {result.stderr}")
            else:
                subprocess.run(f"rm {err_folder}/{dataset}_{n}.err", shell=True, capture_output=True, text=True)
                subprocess.run(f"rm {output_folder}/{dataset}_{n}.out", shell=True, capture_output=True, text=True)
                subprocess.run(f"rm {log_folder}/{dataset}_{n}.log", shell=True, capture_output=True, text=True)
                subprocess.run(f"rm -r {tmp_folder}/file{n}", shell=True, capture_output=True, text=True)
                
        print("Deleted files from tier.")

def check_status_submission(dataset,username, uid, remote_folder_name, redirector,jobs_total, resubmit=False): 
    davixfolder = find_folder(redirector, username, remote_folder_name, dataset, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    print("davix folder is: ", davixfolder)
    file_sizes = get_file_sizes(davixfolder, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    job_success = 0
    successJobTag_list = []
    
    err_folder = os.environ.get('PWD')+ f"/tmp/post_processing/{dataset}/condor/error"
    log_folder = os.environ.get('PWD')+ f"/tmp/post_processing/{dataset}/condor/log"
    out_folder = os.environ.get('PWD')+ f"/tmp/post_processing/{dataset}/condor/output"
    
    for file_name, file_size in file_sizes.items():
            if file_size >= 1000:
                # job_success += 1
                # print(file_name)
                idx_file = file_name.split("_")[-1].replace('.root','')
                job_success += 1
                # print(idx_file)
                successJobTag_list.append(dataset+"_file"+str(idx_file))

                # print(file_name)
    result = subprocess.run("condor_q -af:h ClusterId JobStatus JobTag", shell=True, capture_output=True, text=True)
    runningJobId_list, runningJobStatus_list, runningJobTag_list = [], [], []
    failedJobTag_list = []

    for line in result.stdout.splitlines()[1:]:
        jobId, runStatus, JobTag = line.split()
        if dataset in JobTag and JobTag not in successJobTag_list:
            # if JobTag in successJobTag_list:
            #     print("ATTENTION double counting: ", JobTag)
            runningJobId_list.append(jobId)
            runningJobStatus_list.append(runStatus)
            runningJobTag_list.append(JobTag)
    
    failed_jobs_str = ""
    for n in range(jobs_total):
        job_tag = dataset+"_file"+str(n)
        if job_tag not in runningJobTag_list and job_tag not in successJobTag_list:
            failedJobTag_list.append(job_tag)
            failed_jobs_str += f"{job_tag} "
    if len(failedJobTag_list) != 0:
        print("Failed jobs: ", failed_jobs_str)


    job_failed = len(failedJobTag_list)
    print("Running Jobs: " , running_jobs := sum(1 for status in runningJobStatus_list if status == '2'))
    print("Idle Jobs: ", idle_jobs := sum(1 for status in runningJobStatus_list if status == '1'))
    print("Held Jobs: ", held_jobs := sum(1 for status in runningJobStatus_list if status == '5'))
    print("\033[91mJobs failed: {} ({:.2f}%)\033[0m".format(job_failed, (job_failed/jobs_total)*100))
    print("\033[92mJobs succeeded: {} ({:.2f}%)\033[0m\n".format(job_success, (job_success/jobs_total)*100))
    
    held_jobs_str = ''
    if held_jobs >0:
        for job_tag, job_status in zip(runningJobTag_list, runningJobStatus_list):
            if job_status == '5':
                held_jobs_str += f"{job_tag}"
    print("Held Jobs: ", held_jobs_str)
            
    if held_jobs+ job_failed + job_success + running_jobs + idle_jobs != jobs_total:
        print("!!!!!!!! ERROR: FILES MISSING!!!!!")
        sys.exit(1)
    
    if resubmit : 
        
        resubmit_string = ""
        for num_job,jobTag in enumerate(failedJobTag_list):
            file_label = jobTag.split('_')[-1]
           
            print("...REMOVING condor log, err and out ", file_label, end="\r")
            resubmit_string += f"condor_submit tmp/post_processing/{dataset}/{file_label}/condor.sub; "
            subprocess.run(f"rm {err_folder}/{dataset}_{file_label}.err",shell=True, capture_output=True, text=True)
            subprocess.run(f"rm {log_folder}/{dataset}_{file_label}.log",shell=True, capture_output=True, text=True)
            subprocess.run(f"rm {out_folder}/{dataset}_{file_label}.out",shell=True, capture_output=True, text=True)
            
            davix_file_label =file_label.replace("file","tree_hadd_") + ".root"
            
            if davix_file_label in file_sizes.keys():
                print(f"REMOVED {davix_file_label} from tier")
                result = subprocess.run(f"davix-rm {davixfolder}/{file_name} -E /tmp/x509up_u{uid} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/", shell=True, capture_output=True, text=True)
            
            if num_job > 1000: 
                subprocess.run(resubmit_string, shell=True, capture_output=True, text=True)
                resubmit_string =""
        
        subprocess.run(resubmit_string, shell=True, capture_output=True, text=True)
        print(f"Failed {job_failed} jobs have been resubmitted ")

        

    # if resubmit: 
    #     print(f"Resubmitting {len(failedJobTag_list)} jobs in dataset {dataset}...")
    #     for name in failedJobTag_list:
    #         # idx = str()
    #         subprocess.run(f"rm {err_folder}/{dataset}_{n}.err", shell=True, capture_output=True, text=True)
    #         subprocess.run(f"rm {output_folder}/{dataset}_{n}.out", shell=True, capture_output=True, text=True)
    #         subprocess.run(f"rm {log_folder}/{dataset}_{n}.log", shell=True, capture_output=True, text=True)
    #     print("REMOVED condor log, err and out files ")
    #     subprocess.run(str_resubmit, shell=True, capture_output=True, text=True)
    # if delete_files_fromtier:
    #     print(f"Deleting files from tier for {len(jobs_with_errors_numbers)} jobs with Davix errors in dataset {dataset}...")
    #     jobs_to_delete = [n.replace("file", "") for n in jobs_with_errors_numbers]
    #     print("Files to be deleted:\n "+str(jobs_to_delete))
    #     for n in jobs_to_delete:
    #         davixfolder = find_folder(redirector, username, remote_folder_name, dataset, "/tmp/x509up_u"+str(uid), "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    #         file_name = f"tree_hadd_{n}.root"
    #         print(f"davix-rm {davixfolder}/{file_name} -E /tmp/x509up_u{uid} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
    #         result = subprocess.run(f"davix-rm {davixfolder}/{file_name} -E /tmp/x509up_u{uid} --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/", shell=True, capture_output=True, text=True)
    #         print(result.stdout)
    #         if result.stderr:
    #             print(f"Error: {result.stderr}")
    #         else:
    #             subprocess.run(f"rm {err_folder}/{dataset}_{n}.err", shell=True, capture_output=True, text=True)
    #             subprocess.run(f"rm {output_folder}/{dataset}_{n}.out", shell=True, capture_output=True, text=True)
    #             subprocess.run(f"rm {log_folder}/{dataset}_{n}.log", shell=True, capture_output=True, text=True)
    #             subprocess.run(f"rm -r {tmp_folder}/file{n}", shell=True, capture_output=True, text=True)
                
    #     print("Deleted files from tier.")


# idleJobTag_list
# notRunningJobTag_list = "non sono sul tier & non è in running (la sua JobTag non è tra quelle che stanno girando su condor_q)"  
# successfulJobTag_list = "sono sul tier ed hanno una certa dimensione"
# failedJobTag_list     = "sta qui dentro totalJobTag_list ma non stanno in successfulJobTag_list nè in runningJobTag_list, nè in idle"

# len(successfulJobTag_list)/len(totalJobTag_list)

# # Esempio di utilizzo
# folder = find_folder("Run3Analysis_Tprime", "TprimeToTZ_1800_2022", "/tmp/x509up_u140541", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
# # directory_url = "davs://stwebdav.pi.infn.it:8443/cms/store/user/acagnott/Run3Analysis_Tprime/DataEGammaC_2022/20240703_092359/"
# # cert_path = "/tmp/x509up_u140541"
# # ca_path = "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/"
# file_sizes = get_file_sizes(folder, "/tmp/x509up_u140541", "/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates/")
# for file_name, file_size in file_sizes.items():
#     if file_size <1000:
#         print(f"File: {file_name}, Size: {file_size} bytes")