# -*- coding: utf-8 -*-

import importlib
import inspect

import numpy as np
import sklearn
from sklearn.cluster import (AffinityPropagation, AgglomerativeClustering,
                             Birch, DBSCAN, FeatureAgglomeration, KMeans,
                             BisectingKMeans, MiniBatchKMeans, MeanShift, OPTICS,
                             SpectralClustering, SpectralBiclustering, SpectralCoclustering)
from sklearn.cluster._birch import _CFNode, _CFSubcluster
from sklearn.cluster._bisect_k_means import _BisectingTree

# Allow additional dependencies to be optional
__optionals__ = []


try:
    from imblearn.under_sampling import (ClusterCentroids, CondensedNearestNeighbour, EditedNearestNeighbours,
                                         RepeatedEditedNearestNeighbours, AllKNN, InstanceHardnessThreshold,
                                         NearMiss, NeighbourhoodCleaningRule, OneSidedSelection,
                                         RandomUnderSampler, TomekLinks)
    from imblearn.over_sampling import (RandomOverSampler, SMOTE, SMOTEN, SMOTENC, ADASYN, BorderlineSMOTE,
                                        KMeansSMOTE, SVMSMOTE)
    from imblearn.combine import SMOTEENN, SMOTETomek

    __optionals__.extend(['imblearn'])
except:
    pass

from .utils.random_state import serialize_random_state, deserialize_random_state
from .utils.memory import serialize_memory, deserialize_memory


if 'imblearn' in __optionals__:
    def serialize_cluster_centroids(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'cluster-centroids',
                            'params': {param: value
                                       for param, value in model.get_params().items()
                                       if not param.startswith('estimator')}
                            }

        serialized_model['params']['estimator'] = serialize_model(model.estimator)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'estimator_' in model.__dict__:
            serialized_model['estimator_'] = serialize_model(model.estimator_)
        if 'voting_' in model.__dict__:
            serialized_model['voting_'] = model.voting_

        return serialized_model


    def deserialize_cluster_centroids(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        model_dict['params']['estimator'] = deserialize_model(model_dict['params']['estimator'])

        model = ClusterCentroids(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'estimator_' in model_dict.keys():
            model.estimator_ = deserialize_model(model_dict['estimator_'])
        if 'voting_' in model_dict.keys():
            model.voting_ = model_dict['voting_']

        return model


    def serialize_condensed_nearest_neighbours(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'condensed-nearest-neighbours',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int) and model.n_neighbors is not None:
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'estimator_' in model.__dict__:
            serialized_model['estimator_'] = serialize_model(model.estimator_)
        if 'estimators_' in model.__dict__:
            serialized_model['estimators_'] = [serialize_model(estimator_) for estimator_ in model.estimators_]
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_condensed_nearest_neighbours(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int) and model_dict['params']['n_neighbors'] is not None:
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = CondensedNearestNeighbour(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'estimator_' in model_dict.keys():
            model.estimator_ = deserialize_model(model_dict['estimator_'])
        if 'estimators_' in model_dict.keys():
            model.estimators_ = [deserialize_model(estimator_) for estimator_ in model_dict['estimators_']]
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_edited_nearest_neighbours(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'edited-nearest-neighbours',
                            'params': {param: value
                                       for param, value in model.get_params().items()
                                       if not param.startswith('n_neighbors__')}
                            }

        if not isinstance(model.n_neighbors, int):
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_edited_nearest_neighbours(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int):
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = EditedNearestNeighbours(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_repeated_edited_nearest_neighbours(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'repeated-edited-nearest-neighbours',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int):
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'n_iter_' in model.__dict__:
            serialized_model['n_iter_'] = model.n_iter_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)
        if 'enn_' in model.__dict__:
            serialized_model['enn_'] = serialize_edited_nearest_neighbours(model.enn_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_repeated_edited_nearest_neighbours(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int):
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = RepeatedEditedNearestNeighbours(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'n_iter_' in model_dict.keys():
            model.n_iter_ = model_dict['n_iter_']
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])
        if 'enn_' in model_dict.keys():
            model.enn_ = deserialize_edited_nearest_neighbours(model_dict['enn_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_all_knn(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'all-knn',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int):
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)
        if 'enn_' in model.__dict__:
            serialized_model['enn_'] = serialize_edited_nearest_neighbours(model.enn_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_all_knn(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int):
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = AllKNN(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])
        if 'enn_' in model_dict.keys():
            model.enn_ = deserialize_edited_nearest_neighbours(model_dict['enn_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_instance_hardness_threshold(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'instance-hardness-threshold',
                            'params': model.get_params()
                            }

        if serialized_model['params']['estimator'] is not None:
            serialized_model['params']['estimator'] = serialize_model(model.estimator)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'estimator_' in model.__dict__:
            serialized_model['estimator_'] = serialize_model(model.estimator_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_instance_hardness_threshold(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if model_dict['params']['estimator'] is not None:
            model_dict['params']['estimator'] = deserialize_model(model_dict['params']['estimator'])

        model = InstanceHardnessThreshold(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'estimator_' in model_dict.keys():
            model.estimator_ = deserialize_model(model_dict['estimator_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_near_miss(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'near-miss',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int):
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)
        if not isinstance(model.n_neighbors_ver3, int):
            serialized_model['params']['n_neighbors_ver3'] = serialize_model(model.n_neighbors_ver3)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_near_miss(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int):
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])
        if not isinstance(model_dict['params']['n_neighbors_ver3'], int):
            model_dict['params']['n_neighbors_ver3'] = deserialize_model(model_dict['params']['n_neighbors_ver3'])

        model = NearMiss(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_neighbourhood_cleaning_rule(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'neighbourhood-cleaning-rule',
                            'params': model.get_params()
                            }

        if model.edited_nearest_neighbours is not None:
            serialized_model['params']['edited_nearest_neighbours'] = serialize_model(model.edited_nearest_neighbours)
        if not isinstance(model.n_neighbors, int):
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)
        if 'edited_nearest_neighbours_' in model.__dict__:
            serialized_model['edited_nearest_neighbours_'] = serialize_edited_nearest_neighbours(model.edited_nearest_neighbours_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()
        if 'classes_to_clean_' in model.__dict__:
            serialized_model['classes_to_clean_'] = [int(x) for x in model.classes_to_clean_]

        return serialized_model


    def deserialize_neighbourhood_cleaning_rule(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int):
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])
        if model_dict['params']['edited_nearest_neighbours'] is not None:
            model_dict['params']['edited_nearest_neighbours'] = deserialize_model(model_dict['params']['edited_nearest_neighbours'])

        model = NeighbourhoodCleaningRule(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])
        if 'edited_nearest_neighbours_' in model_dict.keys():
            model.edited_nearest_neighbours_ = deserialize_edited_nearest_neighbours(model_dict['edited_nearest_neighbours_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])
        if 'classes_to_clean_' in model_dict.keys():
            model.classes_to_clean_ = model_dict['classes_to_clean_']

        return model


    def serialize_one_sided_selection(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'one-sided-selection',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int) and model.n_neighbors is not None:
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'estimator_' in model.__dict__:
            serialized_model['estimator_'] = serialize_model(model.estimator_)
        if 'estimators_' in model.__dict__:
            serialized_model['estimators_'] = [serialize_model(estimator_) for estimator_ in model.estimators_]
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_one_sided_selection(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int) and model_dict['params']['n_neighbors'] is not None:
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = OneSidedSelection(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'estimator_' in model_dict.keys():
            model.estimator_ = deserialize_model(model_dict['estimator_'])
        if 'estimators_' in model_dict.keys():
            model.estimators_ = [deserialize_model(estimator_) for estimator_ in model_dict['estimators_']]
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_random_under_sampler(model):
        serialized_model = {'meta': 'random-under-sampler',
                            'params': model.get_params()
                            }

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_random_under_sampler(model_dict):
        from collections import OrderedDict

        model = RandomUnderSampler(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_tomek_links(model):
        from .ml2json import serialize_model

        serialized_model = {'meta': 'tomek-links',
                            'params': model.get_params()
                            }

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()

        return serialized_model


    def deserialize_tomek_links(model_dict):
        from collections import OrderedDict

        model = TomekLinks(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])

        return model


    def serialize_random_over_sampler(model):
        serialized_model = {'meta': 'random-over-sampler',
                            'params': model.get_params()
                            }

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'sample_indices_' in model.__dict__:
            serialized_model['sample_indices_'] = model.sample_indices_.tolist()
        if 'shrinkage_' in model.__dict__:
            serialized_model['shrinkage_'] = model.shrinkage_

        return serialized_model


    def deserialize_random_over_sampler(model_dict):
        from collections import OrderedDict

        model = RandomOverSampler(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'sample_indices_' in model_dict.keys():
            model.sample_indices_ = np.array(model_dict['sample_indices_'])
        if 'shrinkage_' in model_dict.keys():
            model.shrinkage_ = np.array(model_dict['shrinkage_'])

        return model


    def serialize_smote(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'smote',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)

        return serialized_model


    def deserialize_smote(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])

        model = SMOTE(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])

        return model


    def serialize_smotenc(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'smotenc',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)
        if serialized_model['params']['categorical_encoder'] is not None:
            serialized_model['params']['categorical_encoder'] = serialize_model(serialized_model['params']['categorical_encoder'])

        if 'n_features_' in model.__dict__:
            serialized_model['n_features_'] = model.n_features_
        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)
        if 'categorical_encoder_' in model.__dict__:
            serialized_model['categorical_encoder_'] = serialize_model(model.categorical_encoder_) if model.categorical_encoder_ is not None else None
        if 'categorical_features_' in model.__dict__:
            serialized_model['categorical_features_'] = model.categorical_features_.tolist()
        if 'continuous_features_' in model.__dict__:
            serialized_model['continuous_features_'] = model.continuous_features_.tolist()
        if 'median_std_' in model.__dict__:
            serialized_model['median_std_'] = {int(param): float(value) for param, value in model.median_std_.items()}
        if 'ohe_' in model.__dict__:
            serialized_model['ohe_'] = serialize_model(model.ohe_)

        return serialized_model


    def deserialize_smotenc(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if model_dict['params']['categorical_encoder'] is not None:
            model_dict['params']['categorical_encoder'] = deserialize_model(model_dict['params']['categorical_encoder'])
        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])

        model = SMOTENC(**model_dict['params'])

        if 'n_features_' in model_dict.keys():
            model.n_features_ = model_dict['n_features_']
        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])
        if 'categorical_encoder_' in model_dict.keys():
            model.categorical_encoder_ = deserialize_model(model_dict['categorical_encoder_']) if model_dict['categorical_encoder_'] is not None else None
        if 'categorical_features_' in model_dict.keys():
            model.categorical_features_ = model_dict['categorical_features_']
        if 'continuous_features_' in model_dict.keys():
            model.continuous_features_ = model_dict['continuous_features_']
        if 'median_std_' in model_dict.keys():
            model.median_std_ = model_dict['median_std_']
        if 'ohe_' in model_dict.keys():
            model.ohe_ = deserialize_model(model_dict['ohe_'])

        return model


    def serialize_smoten(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'smoten',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)
        if serialized_model['params']['categorical_encoder'] is not None:
            serialized_model['params']['categorical_encoder'] = serialize_model(serialized_model['params']['categorical_encoder'])

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)
        if 'categorical_encoder_' in model.__dict__:
            serialized_model['categorical_encoder_'] = serialize_model(model.categorical_encoder_) if model.categorical_encoder_ is not None else None

        return serialized_model


    def deserialize_smoten(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if model_dict['params']['categorical_encoder'] is not None:
            model_dict['params']['categorical_encoder'] = deserialize_model(model_dict['params']['categorical_encoder'])
        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])

        model = SMOTEN(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])
        if 'categorical_encoder_' in model_dict.keys():
            model.categorical_encoder_ = deserialize_model(model_dict['categorical_encoder_']) if model_dict['categorical_encoder_'] is not None else None

        return model


    def serialize_adasyn(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'adasyn',
                            'params': model.get_params()
                            }

        if not isinstance(model.n_neighbors, int) and model.n_neighbors is not None:
            serialized_model['params']['n_neighbors'] = serialize_model(model.n_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'nn_' in model.__dict__:
            serialized_model['nn_'] = serialize_model(model.nn_)

        return serialized_model


    def deserialize_adasyn(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['n_neighbors'], int) and model_dict['params']['n_neighbors'] is not None:
            model_dict['params']['n_neighbors'] = deserialize_model(model_dict['params']['n_neighbors'])

        model = SMOTE(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'nn_' in model_dict.keys():
            model.nn_ = deserialize_model(model_dict['nn_'])

        return model


    def serialize_borderline_smote(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'borderline-smote',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)
        if not isinstance(model.m_neighbors, int) and model.m_neighbors is not None:
            serialized_model['params']['m_neighbors'] = serialize_model(model.m_neighbors)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'in_danger_indices' in model.__dict__:
            serialized_model['in_danger_indices'] = {int(param): value.tolist()
                                                     for param, value in model.in_danger_indices.items()}
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)
        if 'nn_m_' in model.__dict__:
            serialized_model['nn_m_'] = serialize_model(model.nn_m_)

        return serialized_model


    def deserialize_borderline_smote(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])
        if not isinstance(model_dict['params']['m_neighbors'], int) and model_dict['params']['m_neighbors'] is not None:
            model_dict['params']['m_neighbors'] = deserialize_model(model_dict['params']['m_neighbors'])

        model = BorderlineSMOTE(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'in_danger_indices' in model_dict.keys():
            model.in_danger_indices = {param: np.array(value)
                                       for param, value in model_dict['in_danger_indices'].items()}
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])
        if 'nn_m_' in model_dict.keys():
            model.nn_m_ = deserialize_model(model_dict['nn_m_'])

        return model


    def serialize_kmeans_smote(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'kmeans-smote',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)
        if model.kmeans_estimator is not None:
            serialized_model['params']['kmeans_estimator'] = serialize_model(model.kmeans_estimator)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'kmeans_estimator_' in model.__dict__:
            serialized_model['kmeans_estimator_'] = serialize_model(model.kmeans_estimator_)
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)
        if 'cluster_balance_threshold_' in model.__dict__:
            serialized_model['cluster_balance_threshold_'] = model.cluster_balance_threshold_

        return serialized_model


    def deserialize_kmeans_smote(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])
        if model_dict['params']['kmeans_estimator'] is not None:
            model_dict['params']['kmeans_estimator'] = deserialize_model(model_dict['params']['kmeans_estimator'])

        model = KMeansSMOTE(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'kmeans_estimator_' in model_dict.keys():
            model.kmeans_estimator_ = deserialize_model(model_dict['kmeans_estimator_'])
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])
        if 'cluster_balance_threshold_' in model_dict.keys():
            model.cluster_balance_threshold_ = model_dict['cluster_balance_threshold_']

        return model


    def serialize_svm_smote(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'svm-smote',
                            'params': model.get_params()
                            }

        if not isinstance(model.k_neighbors, int) and model.k_neighbors is not None:
            serialized_model['params']['k_neighbors'] = serialize_model(model.k_neighbors)
        if not isinstance(model.m_neighbors, int) and model.m_neighbors is not None:
            serialized_model['params']['m_neighbors'] = serialize_model(model.m_neighbors)
        if model.svm_estimator is not None:
            serialized_model['params']['svm_estimator'] = serialize_model(model.svm_estimator)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_)
        if 'svm_estimator_' in model.__dict__:
            serialized_model['svm_estimator_'] = serialize_model(model.svm_estimator_)
        if 'nn_k_' in model.__dict__:
            serialized_model['nn_k_'] = serialize_model(model.nn_k_)
        if 'nn_m_' in model.__dict__:
            serialized_model['nn_m_'] = serialize_model(model.nn_m_)
        if 'cluster_balance_threshold_' in model.__dict__:
            serialized_model['cluster_balance_threshold_'] = model.cluster_balance_threshold_

        return serialized_model


    def deserialize_svm_smote(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if not isinstance(model_dict['params']['k_neighbors'], int) and model_dict['params']['k_neighbors'] is not None:
            model_dict['params']['k_neighbors'] = deserialize_model(model_dict['params']['k_neighbors'])
        if not isinstance(model_dict['params']['m_neighbors'], int) and model_dict['params']['m_neighbors'] is not None:
            model_dict['params']['m_neighbors'] = deserialize_model(model_dict['params']['m_neighbors'])
        if model_dict['params']['svm_estimator'] is not None:
            model_dict['params']['svm_estimator'] = deserialize_model(model_dict['params']['svm_estimator'])

        model = SVMSMOTE(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_'])
        if 'svm_estimator_' in model_dict.keys():
            model.svm_estimator_ = deserialize_model(model_dict['svm_estimator_'])
        if 'nn_k_' in model_dict.keys():
            model.nn_k_ = deserialize_model(model_dict['nn_k_'])
        if 'nn_m_' in model_dict.keys():
            model.nn_m_ = deserialize_model(model_dict['nn_m_'])
        if 'cluster_balance_threshold_' in model_dict.keys():
            model.cluster_balance_threshold_ = model_dict['cluster_balance_threshold_']

        return model


    def serialize_smote_enn(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'smote-enn',
                            'params': model.get_params()
                            }

        if model.enn is not None:
            serialized_model['params']['enn'] = serialize_model(model.enn)
        if model.smote is not None:
            serialized_model['params']['smote'] = serialize_model(model.smote)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_) if not isinstance(model.sampling_strategy_, str) else model.sampling_strategy_
        if 'enn_' in model.__dict__:
            serialized_model['enn_'] = serialize_model(model.enn_)
        if 'smote_' in model.__dict__:
            serialized_model['smote_'] = serialize_model(model.smote_)

        return serialized_model


    def deserialize_smote_enn(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if model_dict['params']['enn'] is not None:
            model_dict['params']['enn'] = deserialize_model(model_dict['params']['enn'])
        if model_dict['params']['smote'] is not None:
            model_dict['params']['smote'] = deserialize_model(model_dict['params']['smote'])

        model = SMOTEENN(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_']) if model_dict['sampling_strategy_'] != 'auto' else 'auto'
        if 'enn_' in model_dict.keys():
            model.enn_ = deserialize_model(model_dict['enn_'])
        if 'smote_' in model_dict.keys():
            model.smote_ = deserialize_model(model_dict['smote_'])

        return model


    def serialize_smote_tomek(model):
        from .ml2json import serialize_model
        serialized_model = {'meta': 'smote-tomek',
                            'params': model.get_params()
                            }

        if model.tomek is not None:
            serialized_model['params']['tomek'] = serialize_model(model.tomek)
        if model.smote is not None:
            serialized_model['params']['smote'] = serialize_model(model.smote)

        if 'n_features_in_' in model.__dict__:
            serialized_model['n_features_in_'] = model.n_features_in_
        if 'feature_names_in_' in model.__dict__:
            serialized_model['feature_names_in_'] = model.feature_names_in_
        if 'sampling_strategy_' in model.__dict__:
            serialized_model['sampling_strategy_'] = str(model.sampling_strategy_) if not isinstance(model.sampling_strategy_, str) else model.sampling_strategy_
        if 'tomek_' in model.__dict__:
            serialized_model['tomek_'] = serialize_model(model.tomek_)
        if 'smote_' in model.__dict__:
            serialized_model['smote_'] = serialize_model(model.smote_)

        return serialized_model


    def deserialize_smote_tomek(model_dict):
        from collections import OrderedDict
        from .ml2json import deserialize_model

        if model_dict['params']['tomek'] is not None:
            model_dict['params']['tomek'] = deserialize_model(model_dict['params']['tomek'])
        if model_dict['params']['smote'] is not None:
            model_dict['params']['smote'] = deserialize_model(model_dict['params']['smote'])

        model = SMOTETomek(**model_dict['params'])

        if 'n_features_in_' in model_dict.keys():
            model.n_features_in_ = model_dict['n_features_in_']
        if 'feature_names_in_' in model_dict.keys():
            model.feature_names_in_ = np.array(model_dict['feature_names_in_'][0])
        if 'sampling_strategy_' in model_dict.keys():
            model.sampling_strategy_ = eval(model_dict['sampling_strategy_']) if model_dict['sampling_strategy_'] != 'auto' else 'auto'
        if 'tomek_' in model_dict.keys():
            model.tomek_ = deserialize_model(model_dict['tomek_'])
        if 'smote_' in model_dict.keys():
            model.smote_ = deserialize_model(model_dict['smote_'])

        return model
