import React from 'react'
import PropTypes from 'prop-types'

import Field from '../../Fields/Field'
import ErrorList from '../../ErrorList'
import Spinner from '../../Spinner/Spinner'
import { TextArea } from '@src/components/Form/TextArea'
import { Input } from '@src/components/Form/Input'



export default class Objective extends React.Component {

  constructor(props) {
    super(props)

    this.bindEvents()
  }

  bindEvents() {
    this.handleChange = this.handleChange.bind(this)
    this.deleteObjective = this.deleteObjective.bind(this)
  }

  handleChange(item) {
    this.props.handleChange({
      data: {
        ...this.props.data,
        ...item,
      },
      id: this.props.id
    })
  }

  deleteObjective() {
    this.props.deleteObjective(this.props.data.pk)
  }

  render() {
    const { number, data, isLoading, showSavedMessage, errors } = this.props

    let statusIndicator
    if (isLoading) {
      statusIndicator = <Spinner text="Saving..."/>
    } else if (showSavedMessage) {
      statusIndicator = <p id="objective-saved-message">Changes saved.</p>
    } else {
      statusIndicator = ''
    }

    return (
      <>
        <div className="objective bg-blue-deep-10 radius p-s">
          <div className={`grid objective-fields ${isLoading ? 'loading' : ''}`}>
            <h3 className='body-l-b'>Objective {number}</h3>
              <div className='c-full'>
                <TextArea
                  id='description'
                  placeholder="Add some text"
                  label="Description"
                  value={data.description}
                  onChange={this.handleChange}
                  errors={[]}
                />
                <hr className="hr hr--light" />
              </div>
              <div className="c-1-2">
                <Input
                  id='start_date'
                  type="date"
                  label="Start date"
                  value={data.start_date}
                  onChange={this.handleChange}
                  errors={[]}
                />
              </div>
              <div className="c-1-2">
                <Input
                  id='end_date'
                  type="date"
                  label="End date"
                  value={data.end_date}
                  onChange={this.handleChange}
                  errors={[]}
                />
              </div>
              <div className='c-full'>
                <hr className="hr hr--light" />
                <Input
                  id='owner'
                  placeholder="Add an owner"
                  label="Owner"
                  value={data.owner}
                  onChange={this.handleChange}
                  errors={[]}
                />
              </div>
              <div className='c-full'>
                <hr className="hr hr--light" />
                <TextArea
                  id='planned_reviews'
                  placeholder="Add some text"
                  label="Planned reviews"
                  value={data.planned_reviews}
                  onChange={this.handleChange}
                  errors={[]}
                />
              </div>
          </div>
        </div>
        <button type="button" className="button--delete" onClick={this.deleteObjective}>Delete</button>
        {statusIndicator}
        <ErrorList errors={errors.__all__ || []} />
        <hr/>
      </>
    )
  }

}

Objective.propTypes = {
  handleChange: PropTypes.func.isRequired,
  deleteObjective: PropTypes.func.isRequired,
  number: PropTypes.number.isRequired,
  id: PropTypes.number.isRequired,
  isLoading: PropTypes.bool,
  showSavedMessage: PropTypes.bool,
  errors: PropTypes.shape({
    __all__: PropTypes.arrayOf(PropTypes.string.isRequired),
  }),
  data: PropTypes.shape({
    description: PropTypes.string,
    owner: PropTypes.string,
    planned_reviews: PropTypes.string,
    start_date: PropTypes.string,
    end_date: PropTypes.string,
    companyexportplan: PropTypes.number.isRequired,
    pk: PropTypes.number.isRequired,
  }).isRequired
}

Objective.defaultProps = {
  errors: {__all__: []},
  isLoading: false,
  showSavedMessage: false,
}