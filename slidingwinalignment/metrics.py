from __future__ import print_function, division
import mdtraj as md
from tmtools import tm_align

def my_tm_align(coords1, coords2):
    return tm_align(coords1, coords2, "x"*coords1.shape[0], "x"*coords2.shape[0])

def get_similarity_score(path1, path2, chain1, chain2):
    pdb1 = md.load(path1)
    pdb2 = md.load(path2)
    chain_id_to_index1 = {}
    for chain in pdb1.topology.chains:
        if chain.chain_id not in chain_id_to_index1:
            chain_id_to_index1[chain.chain_id] = chain.index
    CAs1 = pdb1.topology.select(f'name CA and chainid {chain_id_to_index1[chain1]}')
    pdb1_CAs = pdb1.atom_slice(CAs1)
    chain_id_to_index2 = {}
    for chain in pdb2.topology.chains:
        if chain.chain_id not in chain_id_to_index2:
            chain_id_to_index2[chain.chain_id] = chain.index
    CAs2 = pdb2.topology.select(f'name CA and chainid {chain_id_to_index2[chain2]}')
    pdb2_CAs = pdb2.atom_slice(CAs2)
    tm = my_tm_align(pdb1_CAs.xyz.reshape(-1,3)*10, pdb2_CAs.xyz.reshape(-1,3)*10)
    return tm.tm_norm_chain1

def get_similarity_score_local(path1, path2, region1, region2, chain1, chain2):
    pdb1 = md.load(path1)
    pdb2 = md.load(path2)
    chain_id_to_index1 = {}
    for chain in pdb1.topology.chains:
        if chain.chain_id not in chain_id_to_index1:
            chain_id_to_index1[chain.chain_id] = chain.index
    CAs1 = pdb1.topology.select(f'name CA and chainid {chain_id_to_index1[chain1]}')
    CAs1_region = CAs1[region1[0]:region1[1]]
    pdb1_CAs = pdb1.atom_slice(CAs1_region)
    chain_id_to_index2 = {}
    for chain in pdb2.topology.chains:
        if chain.chain_id not in chain_id_to_index2:
            chain_id_to_index2[chain.chain_id] = chain.index
    CAs2 = pdb2.topology.select(f'name CA and chainid {chain_id_to_index2[chain2]}')
    CAs2_region = CAs2[region2[0]:region2[1]]
    pdb2_CAs = pdb2.atom_slice(CAs2_region)
    tm = my_tm_align(pdb1_CAs.xyz.reshape(-1,3)*10, pdb2_CAs.xyz.reshape(-1,3)*10)
    return tm.tm_norm_chain1