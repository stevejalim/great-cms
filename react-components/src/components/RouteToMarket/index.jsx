import React, { useState } from 'react'
import PropTypes from 'prop-types'

import { RouteToMarketSection } from '@src/components/RouteToMarket/RouteToMarketSection'
import Services from '../../Services'

export const RouteToMarket = ({
  fields,
  formData,
  formFields
}) => {

  const [routes, setRoutes] = useState(fields)

  const addTable = () => {
    Services.createRouteToMarket({ ...formFields })
      .then((data) => {
        setRoutes([
          ...routes,
          data
        ])
      })
      .catch(() => {})
  }

  const deleteTable = (id) => {
    Services.deleteRouteToMarket(id)
      .then(() => {
        setRoutes(routes.filter((x) => x.pk !== id))
      })
      .catch(() => {})
  }

  const update = (id, selected) => {
    const field = routes.find(x => x.pk === id)
    const updatedRoutes = routes.map( x => x.pk === id ? { ...x, ...selected} : x )

    setRoutes(updatedRoutes)

    Services.updateRouteToMarket({ ...field, ...selected  })
      .then(() => {})
      .catch(() => {})
  }

  return (
    <>
      {routes.length >=1 && routes.map((field) => RouteToMarketSection({ ...formData, update, deleteTable, field }))}
      <button
        type='button'
        className='button button--large button--icon'
        onClick={addTable}>
        <i className='fas fa-plus-circle' />Add route to market
      </button>
    </>
  )
}

RouteToMarket.propTypes = {
  fields: PropTypes.arrayOf(PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
  ]).isRequired
  ).isRequired,
  formData: PropTypes.shape({
    data:PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string,
        label: PropTypes.string,
        options: PropTypes.arrayOf(PropTypes.string)
      }).isRequired
    ).isRequired,
    example: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired
  }).isRequired,
  formFields: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
  ]).isRequired
}
