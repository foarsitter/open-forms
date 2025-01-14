import classNames from 'classnames';
import PropTypes from 'prop-types';
import React, {useContext} from 'react';
import {useIntl} from 'react-intl';

import DeleteIcon from 'components/admin/DeleteIcon';
import {FeatureFlagsContext} from 'components/admin/form_design/Context';
import DSLEditorNode from 'components/admin/form_design/logic/DSLEditorNode';
import DataPreview from 'components/admin/form_design/logic/DataPreview';
import {ACTION_TYPES} from 'components/admin/form_design/logic/constants';
import Select from 'components/admin/forms/Select';

import {ActionComponent} from './Actions';
import {ActionError, Action as ActionType} from './types';

const Action = ({prefixText, action, errors = {}, onChange, onDelete}) => {
  const intl = useIntl();
  const hasErrors = Object.entries(errors).length > 0;

  const flags = useContext(FeatureFlagsContext);
  const enabledActionTypes = ACTION_TYPES.filter(action => {
    const name = action[0];
    return name === 'fetch-from-service' ? flags.of_service_fetch_enabled : true;
  });

  return (
    <div className="logic-action">
      <div
        className={`logic-action__row ${classNames({'logic-action__row--has-errors': hasErrors})}`}
      >
        <div className="logic-action__actions">
          <DeleteIcon
            onConfirm={onDelete}
            message={intl.formatMessage({
              description: 'Logic rule action deletion confirm message',
              defaultMessage: 'Are you sure you want to delete this action?',
            })}
          />
        </div>

        <div className="logic-action__action">
          <div className="dsl-editor">
            <DSLEditorNode errors={null}>{prefixText}</DSLEditorNode>

            <DSLEditorNode errors={errors.action?.type}>
              <Select
                name="action.type"
                choices={enabledActionTypes}
                translateChoices
                allowBlank
                onChange={onChange}
                value={action.action.type}
              />
            </DSLEditorNode>

            <ActionComponent action={action} errors={errors} onChange={onChange} />
          </div>
        </div>
      </div>

      <div className="logic-action__data-preview">
        <DataPreview data={action} />
      </div>
    </div>
  );
};

Action.propTypes = {
  prefixText: PropTypes.node.isRequired,
  action: ActionType.isRequired,
  errors: ActionError,
  onChange: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
};

export default Action;
