EarlyStopper
============

.. currentmodule:: pykeen.stoppers

.. autoclass:: EarlyStopper
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~EarlyStopper.best_epoch
      ~EarlyStopper.best_metric
      ~EarlyStopper.best_model_path
      ~EarlyStopper.clean_up_checkpoint
      ~EarlyStopper.evaluation_batch_size
      ~EarlyStopper.evaluation_slice_size
      ~EarlyStopper.frequency
      ~EarlyStopper.larger_is_better
      ~EarlyStopper.metric
      ~EarlyStopper.number_results
      ~EarlyStopper.patience
      ~EarlyStopper.relative_delta
      ~EarlyStopper.remaining_patience
      ~EarlyStopper.result_tracker
      ~EarlyStopper.stopped
      ~EarlyStopper.use_tqdm

   .. rubric:: Methods Summary

   .. autosummary::

      ~EarlyStopper.get_summary_dict
      ~EarlyStopper.should_evaluate
      ~EarlyStopper.should_stop

   .. rubric:: Attributes Documentation

   .. autoattribute:: best_epoch
   .. autoattribute:: best_metric
   .. autoattribute:: best_model_path
   .. autoattribute:: clean_up_checkpoint
   .. autoattribute:: evaluation_batch_size
   .. autoattribute:: evaluation_slice_size
   .. autoattribute:: frequency
   .. autoattribute:: larger_is_better
   .. autoattribute:: metric
   .. autoattribute:: number_results
   .. autoattribute:: patience
   .. autoattribute:: relative_delta
   .. autoattribute:: remaining_patience
   .. autoattribute:: result_tracker
   .. autoattribute:: stopped
   .. autoattribute:: use_tqdm

   .. rubric:: Methods Documentation

   .. automethod:: get_summary_dict
   .. automethod:: should_evaluate
   .. automethod:: should_stop
