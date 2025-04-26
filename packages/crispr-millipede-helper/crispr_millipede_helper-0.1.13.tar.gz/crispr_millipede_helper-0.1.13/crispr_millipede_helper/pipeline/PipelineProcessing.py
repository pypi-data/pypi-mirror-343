import json
import pandas as pd
from collections import defaultdict
from typing import List
from copy import deepcopy
import ast
from typing import List, Dict
import os
import fitz
from ..models.pipeline_models import (IndexPairPipelineBean, CountResultOutputPipelineBean, SampleAnnotationPipelineBean, SampleResultModel)

def read_pipeline_output_json(pipeline_output_json_fn):
    with open(pipeline_output_json_fn) as fn:
        pipeline_output_json_dict = json.load(fn)
        
    # TODO: Could process into beans here, or just convert into DefaultDict. I prefer a fully processed structure
    return pipeline_output_json_dict

#
# Recursive function for pre-processing pipeline elements into canonical Python types
#
def process_pipeline_element(pipeline_element):
    if type(pipeline_element) is dict:
        if ('left' in pipeline_element.keys()) and ('right' in pipeline_element.keys()): # THIS IS A PAIR
            return (process_pipeline_element(pipeline_element["left"]), process_pipeline_element(pipeline_element["right"])) # RETURN AS TUPLE
        else: # THIS IS A MAP
            new_dict_wrapper = defaultdict()
            for key in pipeline_element.keys():
                pipeline_subelement = pipeline_element[key]
                new_dict_wrapper[key] = process_pipeline_element(pipeline_subelement)
            return new_dict_wrapper # RETURN AS DEFAULTDICT
    elif type(pipeline_element) is list: # THIS IS AN ARRAY
        new_list_wrapper = list()
        for pipeline_subelement in pipeline_element:
            new_list_wrapper.append(process_pipeline_element(pipeline_subelement))
        return new_list_wrapper # RETURN AS ARRAY
    else:
        return pipeline_element

"""
    IMPORTANT TODO:
    - Handle optional arguments (i.e. surrogate, barcode, read2 arguments). Maybe convert dict to default dict with None as default value
    - Need to ensure that the corresponding sample is the same between different indices of the output types: output_screen_countResults_map, output_screen_editingEfficiencies_map, output_screen_supplementaryFiles_map
        - Can do some assertions, or better yet, build a helper function that converts Maps/Pairs into Dict/
"""
def retrieve_demultiplex_sample_result_model_list(samples_json_selected_local: List[Dict],
    index2_attribute_name="index2",
    index2_attribute_name_backup="barcode_index",
    index1_attribute_name="index1",
    index1_attribute_name_backup="i5_index",
    read1_fn_attribute_name="read1_fn",
    read2_fn_attribute_name="read2_fn",
    output_count_result_attribute_name="output_count_result",
    output_editing_efficiency_dict_attribute_name="output_editing_efficiency_dict",
    output_supplementary_files_dict_attribute_name="output_supplementary_files_dict",
    screen_id_attribute_name="SAMPLE_METADATA_screen",
    protospacer_editing_efficiency_attribute_name="protospacer_editing_efficiency",
    surrogate_editing_efficiency_attribute_name="surrogate_editing_efficiency",
    barcode_editing_efficiency_attribute_name="barcode_editing_efficiency",
    match_set_whitelist_reporter_observed_sequence_counter_series_results_attribute_name="match_set_whitelist_reporter_observed_sequence_counter_series_results",
    mutations_results_attribute_name="mutations_results",
    linked_mutation_counters_attribute_name="linked_mutation_counters",
    protospacer_total_mutation_histogram_pdf_attribute_name="protospacer_total_mutation_histogram_pdf",
    surrogate_total_mutation_histogram_pdf_attribute_name="surrogate_total_mutation_histogram_pdf",
    barcode_total_mutation_histogram_pdf_attribute_name="barcode_total_mutation_histogram_pdf",
    surrogate_trinucleotide_mutational_signature_attribute_name="surrogate_trinucleotide_mutational_signature",
    surrogate_trinucleotide_positional_signature_attribute_name="surrogate_trinucleotide_positional_signature",
    whitelist_guide_reporter_df_attribute_name="whitelist_guide_reporter_df",
    count_series_result_attribute_name="count_series_result"
) -> List[SampleResultModel]:
    sample_result_model_list = []
    for samples_json_selected_local_item in samples_json_selected_local:
        # TODO: Need to store associated sample and participant entity information (i.e. their IDs)
        try:
            index1 = samples_json_selected_local_item["attributes"][index1_attribute_name]
        except KeyError as e:
            index1 = samples_json_selected_local_item["attributes"][index1_attribute_name_backup]

        try:
            index2 = samples_json_selected_local_item["attributes"][index2_attribute_name]
        except KeyError as e:
            index2 = samples_json_selected_local_item["attributes"][index2_attribute_name_backup]
            
        index_pair_pipeline_bean = IndexPairPipelineBean(
                index2 = index2,
                index1 = index1,
                read1_fn = samples_json_selected_local_item["attributes"][read1_fn_attribute_name],
                read2_fn = samples_json_selected_local_item["attributes"][read2_fn_attribute_name]
            )

        sample_annotations_tuple_list = [(attribute_name,samples_json_selected_local_item["attributes"][attribute_name]) for attribute_name in samples_json_selected_local_item["attributes"].keys() if ("SAMPLE" in attribute_name) or ("REPLICATE" in attribute_name)]
        sample_annotations_indices, sample_annotations_values = zip(*sample_annotations_tuple_list)
        
        sample_annotation_pipeline_bean = SampleAnnotationPipelineBean(
            sample_annotations_series = pd.Series(sample_annotations_values, index=sample_annotations_indices)
        )

        count_result_output_pipeline_bean = None
        output_screen_countResults = samples_json_selected_local_item["attributes"].get(output_count_result_attribute_name, None)
        output_screen_editingEfficiencies = samples_json_selected_local_item["attributes"].get(output_editing_efficiency_dict_attribute_name, None)
        output_screen_supplementaryFiles = samples_json_selected_local_item["attributes"].get(output_supplementary_files_dict_attribute_name, None)
        if (output_screen_countResults is not None) and (output_screen_editingEfficiencies is not None) and (output_screen_supplementaryFiles is not None):
            count_result_output_pipeline_bean = CountResultOutputPipelineBean(
                count_result_fn =  output_screen_countResults,
                screen_id = samples_json_selected_local_item["attributes"][screen_id_attribute_name],
                protospacer_editing_efficiency = output_screen_editingEfficiencies[protospacer_editing_efficiency_attribute_name],
                surrogate_editing_efficiency = output_screen_editingEfficiencies[surrogate_editing_efficiency_attribute_name],
                barcode_editing_efficiency = output_screen_editingEfficiencies[barcode_editing_efficiency_attribute_name],

                match_set_whitelist_reporter_observed_sequence_counter_series_results_fn = output_screen_supplementaryFiles[match_set_whitelist_reporter_observed_sequence_counter_series_results_attribute_name],
                mutations_results_fn = output_screen_supplementaryFiles[mutations_results_attribute_name],
                linked_mutation_counters_fn = output_screen_supplementaryFiles[linked_mutation_counters_attribute_name],
                protospacer_total_mutation_histogram_pdf_fn = output_screen_supplementaryFiles[protospacer_total_mutation_histogram_pdf_attribute_name],
                surrogate_total_mutation_histogram_pdf_fn = output_screen_supplementaryFiles[surrogate_total_mutation_histogram_pdf_attribute_name],
                barcode_total_mutation_histogram_pdf_fn = output_screen_supplementaryFiles[barcode_total_mutation_histogram_pdf_attribute_name],
                surrogate_trinucleotide_mutational_signature_fn = output_screen_supplementaryFiles[surrogate_trinucleotide_mutational_signature_attribute_name],
                surrogate_trinucleotide_positional_signature_fn = output_screen_supplementaryFiles[surrogate_trinucleotide_positional_signature_attribute_name],
                whitelist_guide_reporter_df_fn = output_screen_supplementaryFiles[whitelist_guide_reporter_df_attribute_name],
                count_series_result_fn = output_screen_supplementaryFiles[count_series_result_attribute_name],
            )

        sample_result_model = SampleResultModel(
            index_pair_pipeline_bean = index_pair_pipeline_bean,
            count_result_output_pipeline_bean = count_result_output_pipeline_bean,
            sample_annotation_pipeline_bean = sample_annotation_pipeline_bean
        )

        sample_result_model_list.append(sample_result_model)
    return sample_result_model_list
    

def sample_result_model_list_to_dataframe(sample_result_model_list: List[SampleResultModel]) -> pd.DataFrame:
    sample_result_series_list: List[pd.Series] = []
    for sample_result_model in sample_result_model_list:
        indices = []
        values = []
        
        indices.extend(sample_result_model.index_pair_pipeline_bean.__dict__.keys())
        values.extend(sample_result_model.index_pair_pipeline_bean.__dict__.values())
        
        if sample_result_model.count_result_output_pipeline_bean is not None:
            indices.extend(sample_result_model.count_result_output_pipeline_bean.__dict__.keys())
            values.extend(sample_result_model.count_result_output_pipeline_bean.__dict__.values())
        
        indices.extend(sample_result_model.sample_annotation_pipeline_bean.sample_annotations_series.index.values)
        values.extend(sample_result_model.sample_annotation_pipeline_bean.sample_annotations_series.values)
        
        sample_result_series_list.append(pd.Series(values, index=indices))
    return pd.DataFrame(sample_result_series_list)
    

def localize_sample_files(samples_json_selected: List[Dict], localized_dir ="") -> List[Dict]:
    """
        Take FISS sample list structure and localize all files from GCP 
    """
    samples_json_selected_local = []
    
    # Iterate through each sample
    for samples_json_selected_item in samples_json_selected:

        # Copy the entity to modify with the localized filename
        samples_json_selected_item_local = deepcopy(samples_json_selected_item)
        sample_id = samples_json_selected_item["name"]

        # Retrieve the count series
        output_count_result = samples_json_selected_item["attributes"].get("output_count_result", None)
        if output_count_result is not None:
            basename = os.path.join(localized_dir, sample_id + "_" + os.path.basename(output_count_result))
            print(basename)
            if os.path.exists(basename):
                print(f"Exists: {basename}")
            else:    
                os.system(f"gsutil cp -n {output_count_result} {basename}")
            samples_json_selected_item_local["attributes"]["output_count_result"] = basename

        # Retrieving the output editing efficiency (primitive variables, so just need to parse, not download)
        output_editing_efficiency_dict = samples_json_selected_item["attributes"].get("output_editing_efficiency_dict", None)
        if type(output_editing_efficiency_dict) is str:
            output_editing_efficiency_dict = ast.literal_eval(output_editing_efficiency_dict)
        samples_json_selected_item_local["attributes"]["output_editing_efficiency_dict"] = output_editing_efficiency_dict

        # Retrieve the supplementary files (parse variables, then download the files)
        output_supplementary_files_dict = samples_json_selected_item["attributes"].get("output_supplementary_files_dict", None)
        if type(output_supplementary_files_dict) is str:
            output_supplementary_files_dict = ast.literal_eval(output_supplementary_files_dict)
        # Download supplementary files
        output_supplementary_files_dict_local = dict()
        if output_supplementary_files_dict is not None:
            for file_id in output_supplementary_files_dict.keys():
                supp_basename = os.path.join(localized_dir, str(sample_id) + "_" + os.path.basename(output_supplementary_files_dict[file_id]))
                if os.path.exists(supp_basename):
                    print(f"Exists: {supp_basename}")
                else:    
                    os.system(f"gsutil cp -n {output_supplementary_files_dict[file_id]} {supp_basename}")

                splittext = os.path.splitext(supp_basename)

                # If supplementary file is .pdf, convert to PNG and add to local, if not, then just add without conversion
                if splittext[1].lower() == ".pdf":
                    png_basename = os.path.join(localized_dir, splittext[0] + ".png")
                    if os.path.exists(png_basename):
                        print(f"Exists: {png_basename}")
                    else:
                        doc = fitz.open(supp_basename)  # open document
                        for i, page in enumerate(doc):
                            pix = page.get_pixmap()  # render page to an image
                            pix.save(png_basename)
                            break

                    output_supplementary_files_dict_local[file_id] = png_basename
                else:
                    output_supplementary_files_dict_local[file_id] = supp_basename

        samples_json_selected_item_local["attributes"]["output_supplementary_files_dict"] = output_supplementary_files_dict_local

        if output_count_result is not None:
            samples_json_selected_local.append(samples_json_selected_item_local)
        
    return samples_json_selected_local


def retrieve_demultiplex_particpant_sample_result_model_list(input_i5ToBarcodeToSampleInfoVarsMap,input_sampleInfoVarnames, output_screenIdToSampleMap, screen_id) -> List[SampleResultModel]:
    
    input_i5ToBarcodeToSampleInfoVarsMap_processed = process_pipeline_element(input_i5ToBarcodeToSampleInfoVarsMap)
    input_sampleInfoVarnames_processed = process_pipeline_element(input_sampleInfoVarnames)
    output_screenIdToSampleMap_processed = process_pipeline_element(output_screenIdToSampleMap)
    
    total_count_result: int = len(output_screenIdToSampleMap_processed[screen_id])
    
    sample_result_model_list: List[SampleResultModel] = []
    for index in range(0, total_count_result):
        index_pair_pipeline_bean = IndexPairPipelineBean(
                index1 =  output_screenIdToSampleMap_processed[screen_id][index][0]["index1"],
                index2 =  output_screenIdToSampleMap_processed[screen_id][index][0]["index2"],
                read1_fn =  output_screenIdToSampleMap_processed[screen_id][index][0]["read1"],
                read2_fn =  output_screenIdToSampleMap_processed[screen_id][index][0]["read2"]
            )

        sample_annotation_pipeline_bean = SampleAnnotationPipelineBean(
            sample_annotations_series = pd.Series(input_i5ToBarcodeToSampleInfoVarsMap_processed[index_pair_pipeline_bean.index1][index_pair_pipeline_bean.index2], index=input_sampleInfoVarnames_processed)
        )

        sample_result_model = SampleResultModel(
            index_pair_pipeline_bean = index_pair_pipeline_bean,
            sample_annotation_pipeline_bean = sample_annotation_pipeline_bean
        )
        
        sample_result_model_list.append(sample_result_model)
        
    return sample_result_model_list   
