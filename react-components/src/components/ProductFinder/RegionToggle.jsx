import React, { useState } from 'react'
import PropTypes from 'prop-types'

export default function RegionToggle(props){

  const [expand, setExpand] = useState(props.expandAllRegions)

  const countryListToggle = () => {
    setExpand(!expand || props.expandAllRegions)
  }
   return (
      <section>
          <div className="grid">
              <h2 className="region-name h-xs" onClick={countryListToggle}>{props.region}
                <button type="button" className="region-expand icon" onClick={countryListToggle}>{(expand || props.expandAllRegions) ? '-' : '+'}</button>
              </h2>
              <span className={(props.expandAllRegions || expand) ? 'countryList open' : 'countryList'}>
              <hr/>
              <ul>{props.countries}</ul>
              </span>           
          </div>
          <hr className="regionSeperator"/>
        </section>
  )
}
