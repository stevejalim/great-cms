/* eslint-disable */
import React from 'react'
import PropTypes from 'prop-types'

import { slugify } from '../Helpers'


export default class Sector extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      selected: this.props.selected
    }
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(e) {
    this.setState({ selected: !this.state.selected });

    this.props.handleSectorButtonClick(this.props.id);
  }

  render() {
    return (
      <li>
        <button
          className={
            `border-thin border-mid-grey text-mid-grey text-hover-grey bg-hover-stone border-hover-stone pill ${this.state.selected ? 'selected' : ''}`}
          id={this.props.id}
          onClick={this.handleClick}
        >
          {this.props.name}
        </button>
      </li>
    )
  }

}

Sector.propTypes = {
  name: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  selected: PropTypes.bool.isRequired,
}
