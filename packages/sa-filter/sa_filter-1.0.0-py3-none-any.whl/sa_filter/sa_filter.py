# -*- coding: utf-8 -*-

import os
import sys

import pandas as pd
from rdkit import Chem


class SAFilter:
    def __init__(self):
        fname = os.path.relpath(os.path.join(os.path.dirname(__file__), 'data', 'alert_collection.csv'))
        self.rule_df = pd.read_csv(fname)
        # make sure there wasn't a blank line introduced
        self.rule_df = self.rule_df.dropna()
        self.build_rules()

    def build_rules(self) -> None:
        """Parse SMARTS of defined alerts."""
        self.rule_df.loc[:, 'patt'] = None
        for i, row in self.rule_df.iterrows():
            smarts_mol = Chem.MolFromSmarts(row.smarts)
            if smarts_mol:
                self.rule_df.loc[i, 'patt'] = smarts_mol
            else:
                print(f"Error parsing SMARTS for rule {row.rule_id}", file=sys.stderr)

    def get_alert_sets(self) -> list[str]:
        """Get the names of rule sets."""
        return self.rule_df.rule_set_name.unique().tolist()

    def get_alerts(self) -> pd.DataFrame:
        """Get the rule set used for filtering molecules."""
        return self.rule_df.drop(columns='patt')

    def contains_alert(self, smiles_lst: list[str], return_alerts: bool = False) -> list[bool] | list[tuple[str | None, str | None]]:
        """Evaluate structure alerts on a list of SMILES.
        :param smiles_lst: List of SMILES
        :param return_alerts: Obtain the name of the first matched alert
        :return: If `return_alert` is False (default), a list indicating if a structural alert was found in the SMILES at the same index in `smiles_lst`.
        If `return_alert` is True, a list of tuples whose first elements are the alert set name and the second the first matched alert.
        """
        res = []
        for smiles in smiles_lst:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError(f'SMILES cannot be parsed: {smiles}')
            for _, row in self.rule_df.iterrows():
                if len(mol.GetSubstructMatches(row.patt)) > row.max_val:
                    res.append((True, row.rule_set_name, f'{row.description} > {row.max_val:d}')
                               if return_alerts
                               else True)
                    break
            else:
                res.append((False, None, None)
                           if return_alerts
                           else False)
        return res
