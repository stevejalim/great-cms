import React from 'react'
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types'
import { useCookies } from 'react-cookie';

import Services from '@src/Services'

import { connect, Provider } from 'react-redux'
import actions from '@src/actions'
import { getMarkets } from '@src/reducers'

function SelectMarket(props) {
  const { market, setMarket } = props;
  const [cookies] = useCookies(['comparisonMarkets']);

  const clickMarket = (clickedMarket) => {
    setMarket(clickedMarket)
  }

  let isComparisonMarketSelected
  const marketList = Object.values(cookies.comparisonMarkets || {}).map((mapMarket) => {
    const isSelected = (market && market.country_iso2_code) === mapMarket.country_iso2_code
    isComparisonMarketSelected = isComparisonMarketSelected || isSelected
    return (
      <li key={mapMarket.country_iso2_code} className="m-b-xs">
        <button type="button" className={`tag tag--icon ${isSelected ? 'tag--primary' : 'tag--tertiary'} market-${mapMarket.country_iso2_code}`} onClick={() => clickMarket(mapMarket)}>
          {mapMarket.country_name}<i className={`fa ${isSelected ? 'fa-check' :'fa-plus'}`}/>
        </button>
      </li>)
  })
  
  /* eslint-disable react/no-danger */
  const nextSteps = isComparisonMarketSelected ? (
    <section className="bg-red-90 p-h-xl p-v-s">
      <h2 className="h-s text-white p-t-0 p-b-xs">Next steps</h2>
      <div className="flex-grid" dangerouslySetInnerHTML={
        {__html:document.getElementById('next-steps').innerHTML}
      }/>
    </section>
  ) : ''
  /* eslint-enable react/no-danger */

  return Object.keys(marketList).length ? (
    <div>
      <section className="grid bg-blue-deep-100 text-white">
        <div className="c-1-4">&nbsp;</div>
        <div className="c-1-2 p-v-m">
          <h2 className="h-m text-white">Ready to choose a country?</h2>
          <p>Choosing a country for your profile tailors your lessons and Export Plan for a better overall experience.</p>
          <p>Don&apos;t worry, you can change this at any time.</p>
          <ul className="m-b-n-xs">
            {marketList}
          </ul>
        </div>
      </section>
      {nextSteps}
    </div>
  ) : ''
}

SelectMarket.propTypes = {
  market: PropTypes.shape({
    country_name: PropTypes.string,
    country_iso2_code: PropTypes.string,
    region: PropTypes.string
  }),
  setMarket: PropTypes.func.isRequired
}
SelectMarket.defaultProps = {
  market: null
}

const mapStateToProps = (state) => {
  return {
    market: getMarkets(state)
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    setMarket: market => { dispatch(actions.setMarket(market)) }
  }
}

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(SelectMarket)

export default function createSelectMarket({ ...params }) {
  ReactDOM.render(
    <Provider store={Services.store}>
      <ConnectedContainer />
    </Provider>, params.element)
}
