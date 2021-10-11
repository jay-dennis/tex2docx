import os
from shutil import copy2


def unique(list1):
    # initialize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def tex_eqn_ids(fin, eqn_flags=None, cleanup=True):
    if eqn_flags is None:
        eqn_flags = [r"\label{eq:"]
    tempfile = fin.replace(".tex", "_temp.tex")
    copy2(src=fin, dst=tempfile)
    count = 0
    eqn_labels = []
    lookups = []
    eqn_labels2 = []
    eqn_ids = {}
    with open(tempfile) as fp:
        for line in fp:
            count += 1
            # print("Line{}: {}".format(count, line.strip()))
            for a in eqn_flags:
                if a in line:
                    eqn_labels = eqn_labels + [line]
                    lookups = lookups + [a]
    # print("================")
    # for e in eqn_labels:
    #     print(e)
    # print("================")
    for i in range(len(eqn_labels)):
        tempe = eqn_labels[i].split(lookups[i])
        tempe = tempe[1].split(r"}")
        id = tempe[0]
        eqn_labels2 = eqn_labels2 + [lookups[i] + id + "}"]
    eqn_labels2_unique = unique(eqn_labels2)
    if len(eqn_labels2) != len(eqn_labels2_unique):
        print("WARNING")
    id_count = 0
    for e in eqn_labels2_unique:
        id_count += 1
        id = e.split(r"\label")
        eqn_ids[id[1]] = str(id_count)
    print(eqn_ids)
    # print("================")
    if cleanup:
        os.remove(tempfile)
    return eqn_ids


def tex_eqn_number(fin, eqn_ids):
    tempfile = fin.replace(".tex", "_temp.tex")
    count = 0
    with open(fin) as fi:
        with open(tempfile, "wt") as fo:
            for line in fi:
                count += 1
                for id,n in eqn_ids.items():
                    if id in line:
                        print(line)
                        line = line.replace(r"\label" + id, "(" + n + ")")
                        line = line.replace(r"\ref" + id, n)
                        line = line.replace(r"\eqref" + id, "(" + n + ")")
                        print(line)
                fo.write(line)
    return tempfile


def prep_eqns(fin, eqn_flags=None, cleanup=True):
    if eqn_flags is None:
        eqn_flags = [r"\label{eq:"]
    eqn_ids = tex_eqn_ids(fin, eqn_flags=eqn_flags, cleanup=cleanup)
    newfile = tex_eqn_number(fin, eqn_ids)
    return newfile


if __name__ == "__main__":
    filein = "test.tex"
    # eqn_flags = [r"\label{eq:"]
    # eids = tex_eqn_ids(fin=filein, eqn_flags=eqn_flags)
    newfile = prep_eqns(filein)
