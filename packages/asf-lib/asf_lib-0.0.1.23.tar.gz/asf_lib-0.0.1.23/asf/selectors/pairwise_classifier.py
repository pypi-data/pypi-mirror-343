import numpy as np
import pandas as pd
from asf.predictors import AbstractPredictor
from asf.selectors.abstract_model_based_selector import AbstractModelBasedSelector
from asf.selectors.feature_generator import (
    AbstractFeatureGenerator,
)


class PairwiseClassifier(AbstractModelBasedSelector, AbstractFeatureGenerator):
    """
    PairwiseClassifier is a selector that uses pairwise comparison of algorithms
    to predict the best algorithm for a given instance.

    Attributes:
        model_class (ClassifierMixin): The classifier model to be used for pairwise comparisons.
        classifiers (list[ClassifierMixin]): List of trained classifiers for pairwise comparisons.
    """

    def __init__(
        self, model_class, metadata, hierarchical_generator=None, use_weights=True
    ):
        """
        Initializes the PairwiseClassifier with a given model class and hierarchical feature generator.

        Args:
            model_class (ClassifierMixin): The classifier model to be used for pairwise comparisons.
            hierarchical_generator (AbstractFeatureGenerator, optional): The feature generator to be used. Defaults to DummyFeatureGenerator.
        """
        AbstractModelBasedSelector.__init__(
            self, model_class, metadata, hierarchical_generator
        )
        AbstractFeatureGenerator.__init__(self)
        self.classifiers: list[AbstractPredictor] = []
        self.use_weights = use_weights

    def _fit(self, features: pd.DataFrame, performance: pd.DataFrame):
        """
        Fits the pairwise classifiers using the provided features and performance data.

        Args:
            features (pd.DataFrame): The feature data for the instances.
            performance (pd.DataFrame): The performance data for the algorithms.
        """
        assert self.algorithm_features is None, (
            "PairwiseClassifier does not use algorithm features."
        )
        for i, algorithm in enumerate(self.metadata.algorithms):
            for other_algorithm in self.metadata.algorithms[i + 1 :]:
                algo1_times = performance[algorithm]
                algo2_times = performance[other_algorithm]

                diffs = algo1_times < algo2_times
                cur_model = self.model_class()
                cur_model.fit(
                    features,
                    diffs,
                    sample_weight=None
                    if not self.use_weights
                    else np.abs(algo1_times - algo2_times),
                )
                self.classifiers.append(cur_model)

    def _predict(self, features: pd.DataFrame):
        """
        Predicts the best algorithm for each instance using the trained pairwise classifiers.

        Args:
            features (pd.DataFrame): The feature data for the instances.

        Returns:
            dict: A dictionary mapping instance names to the predicted best algorithm.
        """
        predictions_sum = self.generate_features(features)

        return {
            instance_name: [
                (
                    predictions_sum.loc[instance_name].idxmax(),
                    self.metadata.budget,
                )
            ]
            for i, instance_name in enumerate(features.index)
        }

    def generate_features(self, features: pd.DataFrame):
        """
        Generates features for the pairwise classifiers.

        Args:
            features (pd.DataFrame): The feature data for the instances.

        Returns:
            np.ndarray: An array of predictions for each instance and algorithm pair.
        """
        cnt = 0
        predictions_sum = pd.DataFrame(
            0, index=features.index, columns=self.metadata.algorithms
        )
        for i, algorithm in enumerate(self.metadata.algorithms):
            for j, other_algorithm in enumerate(self.metadata.algorithms[i + 1 :]):
                prediction = self.classifiers[cnt].predict(features)
                predictions_sum.loc[prediction, algorithm] += 1
                predictions_sum.loc[~prediction, other_algorithm] += 1
                cnt += 1

        return predictions_sum
