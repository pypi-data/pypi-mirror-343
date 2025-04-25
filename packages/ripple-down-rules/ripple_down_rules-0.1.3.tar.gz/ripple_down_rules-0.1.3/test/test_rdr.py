import importlib
import os
from unittest import TestCase, skip

from typing_extensions import List

from ripple_down_rules.datasets import Habitat, Species
from ripple_down_rules.datasets import load_zoo_dataset
from ripple_down_rules.datastructures import Case, MCRDRMode, \
    Case, CaseAttribute, Category, CaseQuery
from ripple_down_rules.experts import Human
from ripple_down_rules.rdr import SingleClassRDR, MultiClassRDR, GeneralRDR
from ripple_down_rules.utils import render_tree, get_all_subclasses, make_set, flatten_list
from test_helpers.helpers import get_fit_scrdr, get_fit_mcrdr, get_fit_grdr, get_habitat


class TestRDR(TestCase):
    all_cases: List[Case]
    targets: List[str]
    case_queries: List[CaseQuery]
    test_results_dir: str = "./test_results"
    expert_answers_dir: str = "./test_expert_answers"
    generated_rdrs_dir: str = "./test_generated_rdrs"
    cache_file: str = f"{test_results_dir}/zoo_dataset.pkl"

    @classmethod
    def setUpClass(cls):
        # fetch dataset
        cls.all_cases, cls.targets = load_zoo_dataset(cache_file=cls.cache_file)
        cls.case_queries = [CaseQuery(case, "species", target=target, mutually_exclusive=True)
                            for case, target in zip(cls.all_cases, cls.targets)]
        for test_dir in [cls.test_results_dir, cls.expert_answers_dir, cls.generated_rdrs_dir]:
            if not os.path.exists(test_dir):
                os.makedirs(test_dir)

    def test_classify_scrdr(self):
        use_loaded_answers = True
        save_answers = False
        filename = self.expert_answers_dir + "/scrdr_expert_answers_classify"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)

        scrdr = SingleClassRDR()
        cat = scrdr.fit_case(self.case_queries[0], expert=expert)
        self.assertEqual(cat, self.targets[0])

        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file)

    def test_fit_scrdr(self):
        use_loaded_answers = True
        save_answers = False
        draw_tree = False
        filename = self.expert_answers_dir + "/scrdr_expert_answers_fit"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)

        scrdr = SingleClassRDR()
        scrdr.fit(self.case_queries, expert=expert,
                  animate_tree=draw_tree)
        render_tree(scrdr.start_rule, use_dot_exporter=True,
                    filename=self.test_results_dir + f"/scrdr")

        cat = scrdr.classify(self.all_cases[50])
        self.assertEqual(cat, self.targets[50])

        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file)

    def test_write_scrdr_to_python_file(self):
        scrdr = get_fit_scrdr(self.all_cases, self.targets)
        scrdr.write_to_python_file(self.generated_rdrs_dir)
        classify_species_scrdr = scrdr.get_rdr_classifier_from_python_file(self.generated_rdrs_dir)
        for case, target in zip(self.all_cases, self.targets):
            cat = classify_species_scrdr(case)
            self.assertEqual(cat, target)

    def test_write_mcrdr_to_python_file(self):
        mcrdr = get_fit_mcrdr(self.all_cases, self.targets)
        mcrdr.write_to_python_file(self.generated_rdrs_dir)
        classify_species_mcrdr = mcrdr.get_rdr_classifier_from_python_file(self.generated_rdrs_dir)
        for case, target in zip(self.all_cases, self.targets):
            cat = classify_species_mcrdr(case)
            self.assertEqual(make_set(cat), make_set(target))

    def test_write_grdr_to_python_file(self):
        grdr, all_targets = get_fit_grdr(self.all_cases, self.targets)
        grdr.write_to_python_file(self.generated_rdrs_dir)
        classify_animal_grdr = grdr.get_rdr_classifier_from_python_file(self.generated_rdrs_dir)
        for case, case_targets in zip(self.all_cases[:len(all_targets)], all_targets):
            cat = classify_animal_grdr(case)
            for cat_name, cat_val in cat.items():
                if cat_name == "habitats":
                    self.assertEqual(cat_val, case_targets['habitats'])
                elif cat_name == "species":
                    self.assertEqual(cat_val[0], case_targets['species'])

    def test_classify_mcrdr(self):
        use_loaded_answers = True
        save_answers = False
        filename = self.expert_answers_dir + "/mcrdr_expert_answers_classify"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)

        mcrdr = MultiClassRDR()
        cats = mcrdr.fit_case(CaseQuery(self.all_cases[0], "species", target=self.targets[0]),
                              expert=expert)

        self.assertEqual(cats[0], self.targets[0])

        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file)

    def test_fit_mcrdr_stop_only(self):
        use_loaded_answers = True
        draw_tree = False
        save_answers = False
        filename = self.expert_answers_dir + "/mcrdr_expert_answers_stop_only_fit"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)
        mcrdr = MultiClassRDR()
        case_queries = [CaseQuery(case, "species", target=target) for case, target in zip(self.all_cases, self.targets)]
        mcrdr.fit(case_queries, expert=expert, animate_tree=draw_tree)
        render_tree(mcrdr.start_rule, use_dot_exporter=True,
                    filename=self.test_results_dir + f"/mcrdr_stop_only")
        cats = mcrdr.classify(self.all_cases[50])
        self.assertEqual(cats[0], self.targets[50])
        self.assertTrue(len(cats) == 1)
        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file)

    def test_fit_mcrdr_stop_plus_rule(self):
        use_loaded_answers = True
        draw_tree = False
        save_answers = False
        append = False
        filename = self.expert_answers_dir + "/mcrdr_stop_plus_rule_expert_answers_fit"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)
        mcrdr = MultiClassRDR(mode=MCRDRMode.StopPlusRule)
        case_queries = [CaseQuery(case, "species", target=target) for case, target in zip(self.all_cases, self.targets)]
        try:
            mcrdr.fit(case_queries, expert=expert, animate_tree=draw_tree)
        # catch pop from empty list error
        except IndexError as e:
            if append:
                expert.use_loaded_answers = False
                mcrdr.fit(case_queries, expert=expert, animate_tree=draw_tree)
            else:
                raise e
        render_tree(mcrdr.start_rule, use_dot_exporter=True,
                    filename=self.test_results_dir + f"/mcrdr_stop_plus_rule")
        cats = mcrdr.classify(self.all_cases[50])
        self.assertEqual(cats[0], self.targets[50])
        self.assertTrue(len(cats) == 1)
        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file, append=append)

    def test_fit_mcrdr_stop_plus_rule_combined(self):
        use_loaded_answers = True
        save_answers = False
        draw_tree = False
        append = False
        filename = self.expert_answers_dir + "/mcrdr_stop_plus_rule_combined_expert_answers_fit"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)
        mcrdr = MultiClassRDR(mode=MCRDRMode.StopPlusRuleCombined)
        case_queries = [CaseQuery(case, "species", target=target) for case, target in zip(self.all_cases, self.targets)]
        try:
            mcrdr.fit(case_queries, expert=expert, animate_tree=draw_tree)
        # catch pop from empty list error
        except IndexError as e:
            if append:
                expert.use_loaded_answers = False
                mcrdr.fit(case_queries, expert=expert, animate_tree=draw_tree)
            else:
                raise e
        render_tree(mcrdr.start_rule, use_dot_exporter=True,
                    filename=self.test_results_dir + f"/mcrdr_stop_plus_rule_combined")
        cats = mcrdr.classify(self.all_cases[50])
        self.assertEqual(cats[0], self.targets[50])
        self.assertTrue(len(cats) == 1)
        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file, append=append)

    def test_classify_grdr(self):
        use_loaded_answers = True
        save_answers = False
        filename = self.expert_answers_dir + "/grdr_expert_answers_classify"
        expert = Human(use_loaded_answers=use_loaded_answers)
        if use_loaded_answers:
            expert.load_answers(filename)

        grdr = GeneralRDR()

        targets = [self.targets[0], Habitat.land]
        attribute_names = [t.__class__.__name__ for t in targets]
        targets = dict(zip(attribute_names, targets))
        case_queries = [CaseQuery(self.all_cases[0], attribute_name=a, target=t) for a, t in targets.items()]
        cats = grdr.fit_case(case_queries, expert=expert)
        self.assertEqual(cats, targets)

        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, filename)
            expert.save_answers(file)

    def test_fit_grdr(self):
        use_loaded_answers = True
        save_answers = False
        draw_tree = False
        filename = "/grdr_expert_answers_fit"

        grdr, all_targets = get_fit_grdr(self.all_cases, self.targets, draw_tree=draw_tree,
                                         expert_answers_dir=self.expert_answers_dir,
                                         expert_answers_file=filename,
                                         load_answers=use_loaded_answers)
        for rule in grdr.start_rules:
            render_tree(rule, use_dot_exporter=True,
                        filename=self.test_results_dir + f"/grdr_{type(rule.conclusion).__name__}")

        if save_answers:
            cwd = os.getcwd()
            file = os.path.join(cwd, self.expert_answers_dir + filename)
            grdr.expert.save_answers(file)
