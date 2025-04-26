from typing import List, Tuple
import numpy as np
from rdkit import Chem
from .utils import polymol_fom_smiles
from .logger import PFPLOGGER


def create_AtomicPairFingerprint(
    smiles_s: List[str], fp_size: int = 2048, complement: bool = False
) -> List[np.ndarray]:
    """
    Creates a list of AtomicPairFingerprints from a list of SMILES strings.

    Args:
        smiles_s (List[str]): List of SMILES strings.
        fp_size (int, optional): Size of the fingerprint. Defaults to 2048.
        complement (bool, optional): If True, the SMILES strings are patched
            with [H][H] at the beginning and end, should be true if working
            with repeating unit smiles to hide the radicals. Defaults to False.
    Returns:
        List[np.array]: List of AtomicPairFingerprints.
    """
    if complement:
        smiles_list = [("[H]{}[H]".format(smiles)) for smiles in smiles_s]
    else:
        smiles_list = smiles_s

    fingerprint_s = [
        np.array(
            list(
                Chem.rdFingerprintGenerator.GetAtomPairGenerator(
                    fpSize=fp_size
                ).GetFingerprint(polymol_fom_smiles(smiles))
            )
        )
        for smiles in smiles_list
    ]
    return fingerprint_s


def create_RDKFingerprint(
    smiles_s: List[str], fp_size: int = 2048, complement: bool = False
) -> List[np.ndarray]:
    """
    Creates a list of RDKFingerprints from a list of SMILES strings.

    Args:
        smiles_s (List[str]): List of SMILES strings.
        fp_size (int, optional): Size of the fingerprint. Defaults to 2048.
        complement (bool, optional): If True, the SMILES strings are patched
            with [H][H] at the beginning and end, should be true if working
            with repeating unit smiles to hide the radicals. Defaults to False.
    Returns:
        List[np.array]: List of RDKFingerprints.
    """
    if complement:
        smiles_list = [("[H]{}[H]".format(smiles)) for smiles in smiles_s]
    else:
        smiles_list = smiles_s

    fingerprint_s = [
        np.array(Chem.RDKFingerprint(polymol_fom_smiles(smiles), fpSize=fp_size))
        for smiles in smiles_list
    ]
    return fingerprint_s


def merge_bit_fingerprints(
    fingerprints: List[np.ndarray[[-1], bool]],
) -> np.ndarray[[-1], bool]:
    """merges an arbitrary number of bit fingerprints into one by using the or operator

    Args:
        fingerprints (List[np.ndarray[[-1], bool]]): arbitrary number of bit fingerprints with the same length L

    Returns:
        np.ndarray[[-1], bool]: merged fingerprint with length L
    """

    # flatten
    fingerprints = [fp.flatten() for fp in fingerprints]
    # make sure all fingerprints have the same length
    if len(set([len(fp) for fp in fingerprints])) > 1:
        raise ValueError("All fingerprints must have the same length.")

    # make sure all fingerprints are bit fingerprints
    fingerprints = [fp.astype(bool) for fp in fingerprints]

    # merge fingerprints
    merged_fp = np.stack(fingerprints)
    merged_fp = np.any(merged_fp, axis=0)
    return merged_fp


def weight_sum_fingerprints(
    fingerprints: List[np.ndarray[[-1], float]], weights: List[float]
) -> np.ndarray[[-1], float]:
    """sums up a list of fingerprints with weights and returns the weighted sum fingerprint

    Args:
        fingerprints (List[np.ndarray[[-1], float]]): list of fingerprints
        weights (List[float]): list of weights

    Returns:
        np.ndarray[[-1], float]: weighted sum fingerprint

    Raises:
        ValueError: if the number of weights is not the same as the number of fingerprints
        ValueError: if the fingerprints do not have the same length

    Example:
        >>> weight_sum_fingerprints([np.array([1,2,3]), np.array([4,5,6])], [0.5, 0.5])
        np.array([2.5, 3.5, 4.5])
    """

    # flatten
    fingerprints = [fp.flatten() for fp in fingerprints]
    # make sure all fingerprints have the same length L
    if len(set([len(fp) for fp in fingerprints])) > 1:
        raise ValueError("All fingerprints must have the same length.")

    # make sure all weights have the same length as the number of fingerprints
    if len(weights) != len(fingerprints):
        raise ValueError(
            "Number of weights must be the same as the number of fingerprints."
        )

    fingerprints = [fp * weights[i] for i, fp in enumerate(fingerprints)]

    return np.sum(fingerprints, axis=0)


def reduce_fp_set(
    fingerprints: List[np.ndarray[[-1], float]], check_correlation: bool = True
) -> Tuple[
    List[np.ndarray[[-1], float]], np.ndarray[[-1], bool], np.ndarray[[-1], float]
]:
    """
    Reduces a set of fingerprints by removing positions that have identical values across all provided fingerprints.

    Given multiple fingerprints, this function identifies and discards the positions (features)
    that are consistent among all the fingerprints.Secondly it keeps only the first of those position which are
    correlating completely positively or negatively, as they deemed as less informative for certain analyses,
    since they don't contribute to the distinction between fingerprints.

    Args:
        fingerprints (List[np.ndarray]): A list of 1D numpy arrays representing the fingerprints.
        check_correlation (bool, optional): If True, the function will also remove positions that correlate completely
        positive or negatively. Defaults to True.

    Returns:
        Tuple[List[np.ndarray], np.ndarray, np.ndarray]:
            - List[np.ndarray]: A list of reduced 1D numpy arrays where identical positions across all fingerprints have
                been removed.
            - np.ndarray: A boolean mask indicating the positions that were kept (False) or removed (True).
            - np.ndarray: The first fingerprint from the input, prior to any reductions.

    Note:
        This function assumes that all input fingerprints are of the same length. It also logs the percentage
        reduction in fingerprint size, which might be useful for understanding the impact of the reduction on the data.

    Examples: # position 3 is correlating with position 1 (1 is kept) and position 4 is never changing
        >>> fp1 = np.array([0.2, 0.5, 0.2, 0.0])
        >>> fp2 = np.array([0.4, 0.6, 0.4, 0.0])
        >>> fp3 = np.array([0.2, 0.7, 0.2, 0.0])
        >>> reduced_fps, mask, reference_fp = reduce_fp_set(fp1, fp2, fp3)
        >>> print(reduced_fps)  # Lists of reduced fingerprints
        np.array([[0.2, 0.5], [0.4, 0.6], [0.2, 0.7]])
        >>> print(mask)         # Mask used for reduction
        np.array([False, False, True, True])
        >>> print(reference_fp) # Reference fingerprint
        np.array([0.2, 0.5, 0.2, 0.0])
    """

    # Stack the fingerprints to identify common positions
    stacked_fps = np.stack(fingerprints)

    # Identify positions that are the same across all fingerprints
    same_positions = np.all(stacked_fps == stacked_fps[0, :], axis=0)
    # This is a mask for all positions that should be excluded

    # Reduce the fingerprints using the mask
    reduced_fps = stacked_fps[:, ~same_positions]

    if check_correlation:
        # calculate correlation matrix from the transposed fp data
        correlation_matrix = np.corrcoef(reduced_fps.T)

        # Determine columns to keep
        threshold = 0.999999  # Threshold is basically 1 but not exactly due to floating point errors
        n_cols = correlation_matrix.shape[0]
        keep = []

        # Keep track of columns already processed
        processed = set()

        for i in range(n_cols):
            # Skip columns that have already been processed
            if i in processed:
                continue
            # Keep the current column
            keep.append(i)
            for j in range(i + 1, n_cols):
                # If the correlation between columns i and j is above the threshold, mark column j as processed
                if abs(correlation_matrix[i, j]) > threshold:
                    processed.add(j)

        # reduce with the correlation
        reduced_fps = reduced_fps[:, keep]  # keep columns collected in the loop

        # combine the mask with the correlation mask
        mask = same_positions | np.array(
            [i not in keep for i in range(len(same_positions))]
        )

    PFPLOGGER.info(
        "reduced size by {0:.0f}%".format(
            (1 - (len(reduced_fps[0]) / len(fingerprints[0]))) * 100
        )
    )

    # Return the reduced fingerprints, the mask, and a reference fingerprint
    return reduced_fps, mask, fingerprints[0].copy()


def apply_reduction_fp_set(
    fingerprints: List[np.ndarray[[-1], float]],
    mask: np.ndarray[[-1], bool],
    reference_fp: np.ndarray[[-1], float],
) -> List[np.ndarray[[-1], float]]:
    """
    Given multiple fingerprints, this function discards the same positions (features)
    like the reduce_fp_set function did with a prior set, thus rendering the fingerprints comparable.

    Args:
        fingerprints (List[np.ndarray]): A list of 1D numpy arrays representing the fingerprints.
        mask (np.ndarray): A boolean mask indicating the positions that were kept (False) or removed (True).
        reference_fp (np.ndarray): The first fingerprint from the input, prior to any reductions
            (needed for the information loss calculation).

    Returns:
        Tuple[List[np.ndarray], np.ndarray, np.ndarray]:
            - List[np.ndarray]: A list of 1D numpy arrays reduced by the mask.

    Note:
        This function assumes that all input fingerprints and the maske (prior set) are of the same length.
        It also logs the loss which depicts the percentage of information lost by the reduction, respectively positions
         that were new but removed for comparability.

    Examples:
        >>> fp4 = np.array([0.2, 0.6, 0.2])
        >>> fp5 = np.array([0.2, 0.7, 0.1])
        >>> mask = np.array([True, False, True])
        >>> reference_fp = np.array([0.2, 0.5, 0.1])
        >>> reduced_fps= apply_reduction_fp_set([fp4, fp5], mask, reference_fp)
        >>> print(reduced_fps)  # Lists of reduced fingerprints
        np.array([[[0.6], [0.7]])
    """
    is_out_count = mask.sum()
    if is_out_count == 0:
        return fingerprints

    stacked_fps = np.stack(fingerprints)
    should_out = (stacked_fps == reference_fp) & mask
    should_out_count = should_out.sum(1)
    min_should_out = should_out_count.min()
    mean_should_out = should_out_count.mean()

    PFPLOGGER.info(
        "mean reduction loss is %.0f%% with the highest loss per fingerprint beeing %.0f%%",
        (1 - mean_should_out / is_out_count) * 100,
        (1 - min_should_out / is_out_count) * 100,
    )

    return [new_fp[~mask] for new_fp in fingerprints]
