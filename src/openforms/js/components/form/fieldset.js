import {Formio} from 'formiojs';
import {FIELDSET_BASIC} from './edit/tabs';

const FormioFieldSet = Formio.Components.components.fieldset;

class FieldSet extends FormioFieldSet {
    constructor(component, options, data) {
        /* Field sets have both a 'legend' and a 'label' field. The label should be automatically populated to be equal
        to the legend, but this doesn't seem to work in Formio 4.13.x. Since in open-forms we always use the label, in
        this custom fieldset the legend is hidden and automatically filled with the value of the label.
         */
        if (component.label) {
            component.legend = component.label;
        }
        super(component, options, data);
    }

    static editForm(...extend) {
        const parentEditForm = FormioFieldSet.editForm();
        parentEditForm.components[0].components = [
            FIELDSET_BASIC,
            // The 'API' tab is removed, since the only useful attribute it contained was the 'key', but we
            // have this field in the FIELDSET_BASIC tab.
            // TODO: can these tabs below be removed?
            parentEditForm.components[0].components[2], // Conditions tab
            parentEditForm.components[0].components[3], // Logic tab
            parentEditForm.components[0].components[4], // Layout tab
        ];
        return parentEditForm;
    }
}

export default FieldSet;
