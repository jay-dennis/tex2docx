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


def tex_label_ids(fin, id_flags=None, cleanup=True):
    label_flag = r"\label{"
    if id_flags is None:
        id_flags = ["eq:", "eqn:"]
    id_flags = [label_flag + e for e in id_flags]
    tempfile = fin.replace(".tex", "_temp.tex")
    copy2(src=fin, dst=tempfile)
    count = 0
    id_labels = []
    lookups = []
    id_labels2 = []
    ids = {}
    with open(tempfile) as fp:
        for line in fp:
            count += 1
            # print("Line{}: {}".format(count, line.strip()))
            for a in id_flags:
                if a in line:
                    id_labels = id_labels + [line]
                    lookups = lookups + [a]
    # print("================")
    # for e in id_labels:
    #     print(e)
    # print("================")
    for i in range(len(id_labels)):
        tempe = id_labels[i].split(lookups[i])
        tempe = tempe[1].split(r"}")
        id = tempe[0]
        id_labels2 = id_labels2 + [lookups[i] + id + "}"]
    id_labels2_unique = unique(id_labels2)
    if len(id_labels2) != len(id_labels2_unique):
        print("WARNING")
    id_count = 0
    for e in id_labels2_unique:
        id_count += 1
        id = e.split(r"\label")
        ids[id[1]] = str(id_count)
    print(ids)
    # print("================")
    if cleanup:
        os.remove(tempfile)
    return ids


def tex_number_ref(fin, ids, label_prefix=None):
    tempfile = fin.replace(".tex", "_temp.tex")
    # count = 0
    if len(ids) > 0:
        with open(fin) as fi:
            with open(tempfile, "wt") as fo:
                for line in fi:
                    # count += 1
                    for id,n in ids.items():
                        if id in line:
                            print(line)
                            if label_prefix is None:
                                line = line.replace(r"\label" + id, "(" + n + ")")
                            else:
                                line = line.replace(r"\label" + id, label_prefix + n)
                            line = line.replace(r"\ref" + id, n)
                            line = line.replace(r"\eqref" + id, "(" + n + ")")
                            print(line)
                    fo.write(line)
    else:
        tempfile = fin
    return tempfile


def prep_eqns(fin, id_flags=None, cleanup=True):
    if id_flags is None:
        id_flags = ["eq:", "eqn:"]
    ids = tex_label_ids(fin, id_flags=id_flags, cleanup=cleanup)
    midfile = tabularize_eqns(fin, ids, cleanup=cleanup)
    newfile = tex_number_ref(midfile, ids)
    if cleanup:
        os.remove(midfile)
    return newfile


def prep_figs(fin, id_flags=None, cleanup=True):
    if id_flags is None:
        id_flags = ["fig:"]
    ids = tex_label_ids(fin, id_flags=id_flags, cleanup=cleanup)
    newfile = tex_number_ref(fin, ids, label_prefix="Figure ")
    return newfile


if __name__ == "__main__":
    fin = "test.tex"
    # eids = tex_label_ids(fin=fin, id_flags=["eq:", "eqn:"])
    # fids = tex_label_ids(fin=fin, id_flags=["fig:"])
    # newfile = tabularize_eqns(fin, eqn_ids=eids)
    newfile = prep_eqns(fin)
    newfile2 = prep_figs(newfile)
