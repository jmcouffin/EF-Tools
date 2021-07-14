# -*- coding: utf-8 -*-
__title__ = "Select similar categories"
__author__ = "Erik Frits"




#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> IMPORTS
import clr, sys
clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.DB import ( FilteredElementCollector,
                                FilterNumericEquals,
                                FilterElementIdRule,
                                ElementFilter,
                                ElementParameterFilter,
                                LogicalOrFilter,
                                ParameterValueProvider,
                                BuiltInParameter,
                                ElementId,

                                )

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTIONS
def create_filter(key_parameter, element_value):
    """Function to create a RevitAPI filter."""
    f_parameter = ParameterValueProvider(ElementId(key_parameter))
    f_parameter_value = element_value #e.g. element.Category.Id
    f_rule = FilterElementIdRule(f_parameter, FilterNumericEquals(), f_parameter_value)
    filter = ElementParameterFilter(f_rule)
    return filter
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MAIN

def select(mode):
    """Run Super Select: all in model/view based on given mode."""
    #>>>>>>>>>> FILTERS CONTAINER
    list_of_filters = List[ElementFilter]()

    #>>>>>>>>>> GET CURRENT SELECTION
    current_selection_ids = uidoc.Selection.GetElementIds()

    #>>>>>>>>>> LOOP THROUGH SELECTION
    for id in current_selection_ids:
        element = doc.GetElement(id)

        #>>>>>>>>>> CREATE CATEGORY FILTER
        filter = create_filter(key_parameter=BuiltInParameter.ELEM_CATEGORY_PARAM,
                               element_value=element.Category.Id)
        list_of_filters.Add(filter)


    if list_of_filters:
        #>>>>>>>>>> COMBINE FILTERS
        multiple_filters = LogicalOrFilter(list_of_filters)

        #>>>>>>>>>> GET ELEMENTS BASED ON SELECTION MODE
        if mode == "view":
            elems = FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(multiple_filters).ToElementIds()
        elif mode == "model":
            elems = FilteredElementCollector(doc).WherePasses(multiple_filters).ToElementIds()
        else:
            print("ERROR occured: 'wrong mode'.\n Please contact developer.")
            sys.exit()

        #>>>>>>>>>> SET SELECTION
        if elems:
            uidoc.Selection.SetElementIds(List[ElementId](elems))



