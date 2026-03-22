import pickle

def read_fasta( fasta_path, split_char="!", id_field=0):

    seqs = dict()
    with open( fasta_path, 'r' ) as fasta_f:
        count = 0
        for line in fasta_f:
            if line.startswith('>'):
                uniprot_id = line.replace('>', '').strip().split(split_char)[id_field]
                uniprot_id = uniprot_id + "_" + str(count)
                count += 1
                seqs[ uniprot_id ] = ''
            else:
                seq= ''.join( line.split() ).upper().replace("-","")
                seq = seq.replace('U','X').replace('Z','X').replace('O','X')
                seqs[ uniprot_id ] += seq
    example_id=next(iter(seqs))
    print("Read {} sequences.".format(len(seqs)))
    print("Example:\n{}\n{}".format(example_id,seqs[example_id]))

    return seqs


def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=4)

def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)
