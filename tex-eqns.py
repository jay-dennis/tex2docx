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


def tabularize_eqns(fin, eqn_ids, cleanup=True):
    eqn_lookups = ["equation"]
    table_fill = [r"\begin{tabular}{cc}", r" & ", r" \end{tabular}"]
    tempfile = fin.replace(".tex", "_temp.tex")
    fout = fin.replace(".tex", "_temp_out.tex")
    copy2(src=fin, dst=tempfile)
    with open(tempfile, "r") as fp:
        lines = fp.readlines()
    # print(lines)
    # print("======")
    eqn_starts = []
    eqn_ends = []
    eqn_replace = []
    newlines = []
    for e in eqn_lookups:
        eqn_start = r"\begin{" + e + r"}"
        eqn_end = r"\end{" + e + r"}"
        starts = [i for i, n in enumerate(lines) if eqn_start in n]
        ends = [i+1 for i, n in enumerate(lines) if eqn_end in n]
        replace_flag = [False for i in range(len(starts))]
        for i in range(len(starts)):
            temp_eqn_lines = [j for j in range(starts[i], ends[i])]
            # print(temp_eqn_lines)
            # for j in temp_eqn_lines:
            #     print(lines[j])
            # print(".....")
            replace_eqn = False
            for id in eqn_ids.keys():
                label = r"\label" + id
                # print(label)
                for j in temp_eqn_lines:
                    if label in lines[j]:
                        replace_eqn = True
                        # print(lines[j])
            replace_flag[i] = replace_eqn
        eqn_starts = eqn_starts + starts
        eqn_ends = eqn_ends + ends
        eqn_replace = eqn_replace + replace_flag
    print("====")
    print(eqn_starts)
    print(eqn_ends)
    print(eqn_replace)
    for i in range(len(eqn_starts)):
        if eqn_replace[i]:
            temp_eqn_lines = [j for j in range(eqn_starts[i], eqn_ends[i])]
            print(temp_eqn_lines)
            lines[temp_eqn_lines[0]] = lines[temp_eqn_lines[0]].replace(lines[temp_eqn_lines[0]], table_fill[0] + "\n" + lines[temp_eqn_lines[0]])
            for id in eqn_ids.keys():
                label = r"\label" + id
                print(label)
                temp_rep = False
                for j in temp_eqn_lines:
                    if label in lines[j]:
                        lines[j] = lines[j].replace(label, "")
                        temp_rep = True
                if temp_rep:
                    lines[temp_eqn_lines[-1]] = lines[temp_eqn_lines[-1]].replace(lines[temp_eqn_lines[-1]], lines[temp_eqn_lines[-1]] + table_fill[1] + label + "\n" + table_fill[2] + "\n")
    with open(fout, "wt") as fo:
        for line in lines:
            fo.write(line)
    if cleanup:
        os.remove(tempfile)
    return fout


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
    midfile = tabularize_eqns(fin, eqn_ids, cleanup=cleanup)
    newfile = tex_eqn_number(midfile, eqn_ids)
    if cleanup:
        os.remove(midfile)
    return newfile


if __name__ == "__main__":
    filein = "test.tex"
    # eqn_flags = [r"\label{eq:"]
    # eids = tex_eqn_ids(fin=filein, eqn_flags=eqn_flags)
    # newfile = tabularize_eqns(filein, eqn_ids=eids)
    newfile = prep_eqns(filein)
