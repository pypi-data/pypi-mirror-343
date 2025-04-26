import unittest
import polymerfingerprint.polymer_SMILES_parser as psp
from polymerfingerprint import (
    test_polymer_smiles as is_polymer_smiles_valid,
)  # imported as not starting with test_


class TestSMILESParser(unittest.TestCase):
    def test_parse_psmiles_to_explicit_smiles(self):
        test_cases = [
            (
                "[*]CC[*](C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)",
                "[CH2][CH1](C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)",
            ),
            ("*C(C(=O)OC(C(CC)CCCC))C*", "[CH1](C(=O)OC(C(CC)CCCC))[CH2]"),
            ("*CC(c1c(Cl)cccc1)*", "[CH2][CH1](c1c(Cl)cccc1)"),
            ("[*]CC(C)([*])(C(=O)OC)", "[CH2][C](C)(C(=O)OC)"),
            ("[*]OC(CC)CC(=O)*", "[O]C(CC)C[C](=O)"),
            ("*C(=O)CC(CCC)O*", "[C](=O)CC(CCC)[O]"),
            ("[*]CC([*])(C)(C(=O)OC)", "[CH2][C](C)(C(=O)OC)"),
            ("*OC(CCC(c1ccccc1))CC(=O)O*", "[O]C(CCC(c1ccccc1))CC(=O)[O]"),
            ("*CC([*])(C)(C#N)", "[CH2][C](C)(C#N)"),
            ("[*]CC([*])(c1ccccc1)", "[CH2][CH1](c1ccccc1)"),
            ("[*]CC[*](C)(C(=O)Oc1ccccc1)", "[CH2][C](C)(C(=O)Oc1ccccc1)"),
            ("[*]C1=CC=C([*])(N1)", "[C]1=CC=[C](N1)"),
        ]

        for psmiles, expected in test_cases:
            with self.subTest(psmiles=psmiles):
                result = psp.p_to_explicit_smiles(psmiles)
                self.assertTrue(is_polymer_smiles_valid(result))
                self.assertEqual(result, expected)

    def test_convert_explicit_smiles_to_psmiles(self):
        test_cases = [
            (
                "[CH2][C](C)(C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)",
                "[*]CC([*])(C)(C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)",
            ),
            ("[O]CCC[C](=O)", "[*]OCCCC([*])(=O)"),
            ("[O]CCC[C]", "[*]OCCCC[*]"),
            ("[C]CCC[C]", "[*]CCCCC[*]"),
            ("C([CH])CSC[CH2]", "C(C([*]))CSCC[*]"),
        ]

        for explicit_smiles, expected in test_cases:
            with self.subTest(explicit_smiles=explicit_smiles):
                result = psp.explicit_to_psmiles(explicit_smiles)
                self.assertEqual(result, expected)

    def test_manual_verification_warning(self):
        explicit_smiles = "[CH2][C](C)(C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)"
        expected_psmiles = "[*]CC([*])(C)(C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C)"
        expected_warning = (
            f"Too many OR little explicits found for\n{explicit_smiles}"
            f". Manual verification needed: Is\n{expected_psmiles} the right replacement?"
        )

        with self.assertWarns(UserWarning) as warning:
            result = psp.explicit_to_psmiles(explicit_smiles)
            self.assertEqual(result, expected_psmiles)

        # asserting the logging output
        self.assertIn(expected_warning, str(warning.warning))


if __name__ == "__main__":
    unittest.main()
