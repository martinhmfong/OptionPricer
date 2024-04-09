import React, { useState } from 'react';
import PricerChoice from "./PricerChoice";
import ParameterSetter from "./ParameterSetter";

const OptionPricer = () => {
  const default_parameters = {
    r: null,
    t: null,
    s: null,
    sigma: null,
    s2: null,
    sigma2: null,
    rho: null,
    q: null,
    k: null,
    option_type: "Call",
    mean_method: "Arithmetic",
    option_price: null,
    n: null,
    m: null,
    is_control_variate: false,
    use_simulation: false,
    barrier_low: null,
    barrier_high: null,
    rebate: null,
  }

  const [parameters, setParameters] = useState(default_parameters);
  const [pricer, setPricer] = useState('European')
  const [result, setResult] = useState(null);


  const calculateOptionPrice = async () => {
    await fetch(
      `/price/${pricer}`,
      {
        mode: "no-cors",
        method: "POST",
        body: JSON.stringify(parameters),
      })
      .then(response => response.json())
      .then(result => setResult(result.price))
    // setResult(price);
  };

  return (
    <div className="option-pricer">
      <div className="option-pricer-left">
        <PricerChoice pricer={pricer} setPricer={setPricer}/>
      </div>
      <div>
        <ParameterSetter pricer={pricer} parameters={parameters} setParameters={setParameters}/>
      </div>
      <div className="option-pricer-right">
        <button onClick={calculateOptionPrice}>Calculate</button>
      </div>
      <div className="option-pricer-result">
        {result !== null ? `Option Price: ${result.toFixed(6)}` : ''}
      </div>
    </div>
  );
};

export default OptionPricer;