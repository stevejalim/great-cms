import React, { memo } from 'react'
import PropTypes from 'prop-types'

import { Input } from '@src/components/Form/Input'
import { Select } from '@src/components/Form/Select'
import EducationalMomentTooltip from '../../EducationalMomentTooltip'

export const GrossPrice = memo(({
  country,
  countryGrossUnit,
  profitPerUnit,
  potentialPerUnit,
}) => (
  <>
    <div className='bg-white radius p-xs c-full m-b-s gross-price'>
      <div className=''>
        <i className='fas fa-tag text-blue-deep-60 fa-lg' />
        <p className='m-t-xxs m-b-0'>Gross price per unit for the {country}</p>
        <h3 className='h-s p-t-0 p-b-0'>{countryGrossUnit}</h3>
      </div>
      <hr className='hr--light m-v-xs' />
      <div className=''>
        <p className='m-t-xxs m-b-0'>Gross price per unit in invoicing currency</p>
        <EducationalMomentTooltip
          description='asdasdad'
        />
        <div className='grid'>
          <div className='w-full'>
            <div className='c-1-6 m-r-xs'>
              <Select label='select unit' update={() => {}} name='test' options={[]} hideLabel />
            </div>
            <div className='c-1-3'>
              <Input label='number of units' hideLabel />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div className='grid'>
      <div className='c-1-2'>
        <div className='bg-white radius p-xs'>
          <i className='fas fa-pound-sign text-blue-deep-60 fa-lg' />
          <p className='m-t-xxs m-b-0'>Your profit per unit</p>
          <h3 className='h-s p-t-0 p-b-0'>{profitPerUnit}</h3>
        </div>
      </div>
      <div className='c-1-2'>
        <div className='bg-white radius p-xs'>
          <i className='fas fa-pound-sign text-blue-deep-60 fa-lg' />
          <p className='m-t-xxs m-b-0'>Your potential per unit</p>
          <h3 className='h-s p-t-0 p-b-0'>{potentialPerUnit}</h3>
        </div>
      </div>
    </div>
  </>
))

GrossPrice.propTypes = {
  country: PropTypes.string.isRequired,
  countryGrossUnit: PropTypes.string.isRequired,
  profitPerUnit: PropTypes.string.isRequired,
  potentialPerUnit: PropTypes.string.isRequired
}


