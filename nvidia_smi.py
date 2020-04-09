

def parse_nvidia_smi(line_list, num_gpu):
    beg_line = 7
    status_list = list()
    version_dict = parse_version(line_list[2])
    for n in range(num_gpu):
        info_line1 = line_list[beg_line+3*n]
        info_line2 = line_list[beg_line+3*n+1]
        status_list.append(parse_status(info_line2))
    return version_dict, status_list

def parse_version(line):
    info_list = line.split(' ')
    NVIDIA_SMI = info_list[2]
    Driver = info_list[8]
    CUDA = info_list[14]
    return {
        'NVIDIA_SMI': NVIDIA_SMI,
        'Driver': Driver,
        'CUDA': CUDA,
    }

def parse_status(line):
    info_list = line.split('|')
    info_list1 = info_list[1].lstrip().rstrip().split(' ')
    info_list2 = info_list[2].lstrip().rstrip().split(' ')
    info_list3 = info_list[3].lstrip().rstrip().split(' ')
    GPU_Fan = info_list1[0]  # 79%
    Mem_Use = info_list2[0]  # 3494MiB
    Mem_All = info_list2[2]  # 10986MiB
    Mem_Fra = info_list3[0]  # 97% --> Volatile GPU-Util
    return {
        'GPU_Fan': GPU_Fan,
        'Mem_Use': Mem_Use,
        'Mem_All': Mem_All,
        'Mem_Fra': Mem_Fra,
    }
    # return GPU_Fan, Mem_Use, Mem_All, Mem_Fra






def _demo():
    return \
    '+-----------------------------------------------------------------------------+\n' \
    '| NVIDIA-SMI 418.87.00    Driver Version: 418.87.00    CUDA Version: 10.1     |\n' \
    '|-------------------------------+----------------------+----------------------+\n' \
    '| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |\n' \
    '| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |\n' \
    '|===============================+======================+======================|\n' \
    '|   0  GeForce RTX 208...  Off  | 00000000:01:00.0  On |                  N/A |\n' \
    '| 79%   82C    P2   249W / 250W |   3494MiB / 10986MiB |     97%      Default |\n' \
    '+-------------------------------+----------------------+----------------------+\n' \
    '|   1  GeForce RTX 208...  Off  | 00000000:02:00.0 Off |                  N/A |\n' \
    '| 46%   64C    P2   155W / 250W |   3512MiB / 10989MiB |     30%      Default |\n' \
    '+-------------------------------+----------------------+----------------------+\n' \
    '                                                                               \n' \
    '+-----------------------------------------------------------------------------+\n' \
    '| Processes:                                                       GPU Memory |\n' \
    '|  GPU       PID   Type   Process name                             Usage      |\n' \
    '|=============================================================================|\n' \
    '|    0       948      G   /usr/lib/xorg/Xorg                           160MiB |\n' \
    '|    0      2084      G   /opt/teamviewer/tv_bin/TeamViewer              6MiB |\n' \
    '|    0      2280      G   compiz                                       124MiB |\n' \
    '|    0      6251      C   python                                      3199MiB |\n' \
    '|    1      8706      C   python                                      3501MiB |\n' \
    '+-----------------------------------------------------------------------------+\n'

