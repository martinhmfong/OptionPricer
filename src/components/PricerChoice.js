import React from 'react';

const PriceSelector = (prop) => {
  const pricer_names = ["European", "ImpliedVolatility", "Asian", "Basket", "American", "KIKO"]
  const handlePricerChange = (event) => prop.setPricer(event.target.value)
  return (
    <div>
      <h3>Select a pricer:</h3>
      {pricer_names.map((choice) => (
        <div key={choice}>
          <input
            type="radio"
            key={choice}
            name={choice}
            value={choice}
            checked={choice === prop.pricer}
            onChange={handlePricerChange}
          />
          <label htmlFor={choice}>{choice}</label>
        </div>
      ))}
      <br />
    </div>
  );
};

export default PriceSelector;