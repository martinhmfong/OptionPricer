import React, { useState } from 'react';
import PricerChoice from "./PricerChoice";
import ParameterSetter from "./ParameterSetter";
import ActionButton from "./ActionButton";
import ResultDisplay from "./ResultDisplay";

const OptionPricer = () => {
  const default_parameters = {
    r: 0.05,
    t: 3,
    s: 100,
    sigma: 0.3,
    s2: 100,
    sigma2: 0.3,
    rho: 0.5,
    q: 0,
    k: 100,
    option_type: "Call",
    mean_method: "Arithmetic",
    option_price: null,
    n: 50,
    m: 10000,
    is_control_variate: false,
    use_simulation: false,
    barrier_low: null,
    barrier_high: null,
    rebate: null,
  }

  const [parameters, setParameters] = useState(default_parameters)
  const [pricer, setPricer] = useState('European')
  const [result, setResult] = useState({})


  const calculateOptionPrice = async () => {
    await fetch(
      `/price/${pricer}`,
      {
        mode: "no-cors",
        method: "POST",
        body: JSON.stringify(parameters),
      })
      .then(response => response.json())
      .then(result => setResult(result))
    // setResult(price);
  };

  return (
    <div>
      <h1>FITE7405 Pricer</h1>
      <PricerChoice pricer={pricer} setPricer={setPricer}/>
      <ParameterSetter pricer={pricer} parameters={parameters} setParameters={setParameters}/>
      <ActionButton parameters={parameters} calculateOptionPrice={calculateOptionPrice}/>
      <ResultDisplay result={result} setResult={setResult}/>
    </div>
  );
};

export default OptionPricer;