"""This library of functions withholds the functionality to
 - partially correct and
 - translate between styles of SMILES strings for Polymers
Upon conversion some manual inspection might be necessary and will be demanded for by a warning

The two styles of SMILES strings are:
  - explicit SMILES strings
    - postulated by Köster et al.
    - describe polymer repetition units with radical endings e.g. [CH2]
    - a dimer is created by concatenation of exp SMILES strings
  - polymer SMILES strings (PSMILES)
    - postulated by the Ramprasad-Group
    - describe the linkage of monomers with a star symbol e.g. [*]
    - a dimer is created by substitution of a * in a PSMILES string with another PSMILES string"""

import re
from rdkit import Chem
import warnings
from contextlib import contextmanager


@contextmanager
def custom_warning_format():  # make the warnings more readable
    original_formatwarning = warnings.formatwarning
    warnings.formatwarning = (
        lambda msg, *args, **kwargs: f"SMILESParserWarning: {msg}\n"
    )
    try:
        yield
    finally:
        warnings.formatwarning = original_formatwarning


def p_to_explicit_smiles(psmiles_to_parse: str) -> str:
    """
    Translates Polymer SMILES (PSMILES) codes to explicit SMILES codes, ensuring proper curation and formatting.

    Args:
        psmiles_to_parse (str): The Polymer SMILES string to be translated.

    Returns:
        str: The translated explicit SMILES string.
    """

    def find_side_chain_to_left(psmiles: str, star_pos: int) -> str:
        if ")([*])" not in psmiles:
            return psmiles
        stack = []
        side_chain = []
        r_star_pos = len(psmiles) - star_pos  # reverse the position
        for pos, i in enumerate(reversed(psmiles)):
            if i == ")":
                stack.append(pos)
            if i == "(":
                if len(stack) == 1:
                    side_chain.append((stack.pop(), pos))
                    # when the side chain of the star is left we do not need to keep collecting other side chains
                    if psmiles[-pos - 2] != ")":
                        for nr, side in enumerate(
                            side_chain
                        ):  # sort the side chain so the one with the star is first
                            if r_star_pos in range(side[0], side[1] + 1):
                                side_chain = (
                                    [side_chain[nr]]
                                    + side_chain[nr + 1 :]
                                    + side_chain[:nr]
                                )
                                break
                        else:  # if the star is not in the side chain
                            # reset the collection and continue with next side chain
                            side_chain = []
                            continue
                        break
                else:
                    stack.pop()

        end_chain = -min(min(side_chain))
        if end_chain == 0:
            end_chain = None

        ordered_side_chain_string = "".join(
            [
                psmiles[-end - 1 : -start] if start != 0 else psmiles[-end - 1 :]
                for start, end in side_chain
            ]
        )
        # how print anything else beside the ordered side chains:
        if end_chain:
            return (
                psmiles[: -max(max(side_chain)) - 1]
                + ordered_side_chain_string
                + psmiles[end_chain:]
            )
        else:
            return psmiles[: -max(max(side_chain)) - 1] + ordered_side_chain_string

    def harmonize_PSMILES(psmiles: str) -> str:
        # make sure all stars are enclosed in square brackets but not double enclosed
        corr_enclosed = psmiles.count("[*]")
        if corr_enclosed < 2:
            if corr_enclosed == 0:
                psmiles = psmiles.replace("*", "[*]")
            else:
                front_a = psmiles.find("*")
                if (
                    psmiles.find("[*]") > front_a
                ):  # in case the first star is un-enclosed
                    psmiles = psmiles.replace("*", "[*]", 1)
                else:
                    psmiles = (
                        psmiles.rpartition("*")[0] + "[*]" + psmiles.rpartition("*")[2]
                    )

        # check if the asterisks are set as a side chain if they are not on the end and parenthesize them otherwise.
        second_star_q = 0
        for pos, symbol in enumerate(psmiles):
            if symbol == "*":
                if second_star_q == 0:  # skip the first star
                    second_star_q = 1
                else:  # bracket the second star if necessary
                    if pos == len(psmiles) - 2:
                        # if the asterisk is at the end (before its square bracket)
                        # AND not on a side chain (a ")" before it) it does not need bracketing
                        if psmiles[pos - 2] == ")":
                            psmiles = psmiles[: pos - 1] + "([" + psmiles[pos] + "])"

                    else:
                        if psmiles[pos - 2] != "(" and psmiles[pos + 2] != ")":
                            psmiles = (
                                psmiles[: pos - 1]
                                + "(["
                                + psmiles[pos]
                                + "])"
                                + psmiles[pos + 2 :]
                            )
                    psmiles = find_side_chain_to_left(psmiles, pos)
                    break
        return psmiles

    h_psmiles = harmonize_PSMILES(psmiles_to_parse)

    # second create a mol object
    mol = Chem.MolFromSmiles(h_psmiles)
    if mol is None:
        print(
            f"{psmiles_to_parse} harmonized to {h_psmiles} is not a valid PSMILES string "
            f"for parsing to explicit SMILES"
        )
        return ""

    # iterate over the atoms catching the position of the C Atoms following and preceding [*] and their valence
    star_index = []
    valence = []
    atomsymbols = []
    for atom in mol.GetAtoms():
        atomsymbol = atom.GetSymbol()
        # if atom.GetIsAromatic():
        #     atomsymbol = atomsymbol.lower()
        atomsymbols.append(atomsymbol)
        if atomsymbol == "*":
            star_index.append(atom.GetIdx())
        valence.append(atom.GetExplicitValence())

    if len(star_index) != 2:
        # raise a type error
        raise TypeError(
            f"{__name__} cannot handle (ladder) polymers with {len(star_index)} * in the PSMILES "
            f'"{psmiles_to_parse}" string!'
        )

    c_index = [
        star_index[0] + 1,
        star_index[1] - 1,
    ]  # cannot do that atom symbols are not in order

    # the current valence of the C atoms is the explicit minus the [*] connection/-1
    def valence_change(val):
        return 4 - val

    h_num = []
    for sy, val in zip(atomsymbols, valence):  # number of H atoms assuming C atoms
        if sy == "C":
            h_num.append(valence_change(val))
        else:
            h_num.append(0)

    # replace C atoms with the explicit hydrogen count and catch the special case of parenthesised like e.g.([*]) and
    # parenthesise the dangling part of the smiles string to the end after that C atom like [*]CC([*])(C)C(=O)OC ->
    # [CH2][C](C)(C(=O)OC) (attention to the bracket pair ending with the last symbol ")")

    atomsymbols = [
        _atom if _atom != "*" else r"\*" for _atom in atomsymbols
    ]  # escape the * for the regex

    # create a dict of atom index and index of it's symbol in the string
    atom_positions = [
        m.start()
        for m in re.finditer(r"(" + "|".join(atomsymbols) + ")", h_psmiles.upper())
    ]
    atom_string_map = {
        atom_symbol_nr: string_pos
        for atom_symbol_nr, string_pos in zip(range(len(atomsymbols)), atom_positions)
    }
    c_str_indexes = [atom_string_map[_c_index] for _c_index in c_index]
    c_str_h_num = {
        atom_string_map[_c_index]: h_num[_c_index] for _c_index in c_index
    }  #

    smiles_reconstruction = ""
    for idx, character in enumerate(h_psmiles):
        if idx in c_str_indexes:
            smiles_reconstruction += (
                f"[CH{c_str_h_num[idx]}]" if c_str_h_num[idx] > 0 else f"[{character}]"
            )
        else:
            smiles_reconstruction += character

    # throw warning if the star is not directly behind the monomer-connecting C atom
    if ")[*]" in smiles_reconstruction:
        print(
            f"{psmiles_to_parse} has a star not directly behind the monomer-connecting C atom!"
        )

    smiles_reconstruction = smiles_reconstruction.replace("([*])", "")
    smiles_reconstruction = smiles_reconstruction.replace("[*]", "")

    return smiles_reconstruction


def explicit_to_psmiles(explicit_SMILES: str, chain_pos: str = "monomer"):
    """
    Converts an explicit SMILES string to a Polymer SMILES (PSMILES) string.

    Args:
        explicit_SMILES (str): The explicit SMILES string to be converted.
        chain_pos (str): The position of the chain in the polymer, either "monomer" or "end". Defaults to "monomer".

    Returns:
        str: The converted PSMILES string.
    """
    if not isinstance(explicit_SMILES, str):
        raise TypeError(
            f"explicit_SMILES must be a string, got {type(explicit_SMILES).__name__}"
        )

    all_explicits = re.findall(r"\[[^\]\*]*\]", explicit_SMILES)
    replacements = [
        radical.replace("[", "").replace("]", "") for radical in all_explicits
    ]
    replacements = [re.sub("H[0-9]?", "", radical) for radical in replacements]
    if len(all_explicits) == 0:
        with custom_warning_format():
            warnings.warn(f"No explicits found in {explicit_SMILES}")
        return explicit_SMILES
    PSMILES = explicit_SMILES

    # if the replacement is not at the end or beginning it needs brackets
    end_q = [
        (PSMILES.find(expl) == 0 or PSMILES.rfind(expl) == (len(PSMILES) - len(expl)))
        for expl in all_explicits
    ]

    first = True
    for edge, expl, repl in zip(end_q, all_explicits, replacements):
        if first:
            if edge:
                repl = "[*]" + repl
                first = False
            else:
                repl = repl + "([*])"
                first = False
            PSMILES = PSMILES.replace(expl, repl, 1)
        else:
            if edge:
                repl = repl + "[*]"
            else:
                repl = repl + "([*])"
            PSMILES = PSMILES.replace(expl, repl, 1)
            break

    match chain_pos:
        case "monomer":
            if (
                len(all_explicits) != 2
            ):  # "Is there a radical in the monomer, or is this an end group?"
                with custom_warning_format():
                    warnings.warn(
                        "Too many OR little explicits found for"
                        + "\n"
                        + explicit_SMILES
                        + ". Manual verification needed: Is"
                        + "\n"
                        + PSMILES
                        + " the right replacement?"
                    )
        case "end":
            if (
                len(all_explicits) != 1
            ):  # "Is there a radical in the end group, or is it a monomer?"
                with custom_warning_format():
                    warnings.warn(
                        "None or too many explicits found for"
                        + "\n"
                        + explicit_SMILES
                        + ". Is"
                        + "\n"
                        + PSMILES
                        + " the right replacement?"
                    )

    return PSMILES
