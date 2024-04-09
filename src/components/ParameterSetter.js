import React from 'react';

const ParameterSetter = (prop) => {
  const display_params = {
    European: ["r", "t", "s", "sigma", "q", "k", "option_type"],
    ImpliedVolatility: ["r", "t", "s", "q", "k", "option_type", "option_price"],
    Asian: ["r", "t", "s", "sigma", "k", "option_type", "mean_method", "n", "m", "is_control_variate"],
    Basket: ["r", "t", "s", "sigma", "s2", "sigma2", "k", "option_type", "mean_method", "m", "is_control_variate"],
    American: ["r", "t", "s", "sigma", "k", "option_type", "n"],
    KIKO: ["r", "t", "s", "sigma", "k", "option_type", "n", "m", "barrier_low", "barrier_high", "rebate"],
  }
  // todo set the use simulation to false/true
  const handleParameterChange = (event) => {
    const { name, value } = event.target;
    prop.setParameters((prevParameters) => ({
      ...prevParameters,
      [name]: parseFloat(value),
    }));
  };
  const show_parameters = display_params[prop.pricer]
  return (
    <table>
      <tbody>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
      {show_parameters.map(i => (
        <tr>
          <td>{i}</td>
          <td>
            <input type="number"
                   name={i}
                   key={i}
                   value={prop.parameters[i]}
                   onChange={handleParameterChange}
            />
          </td>
        </tr>
      ))}
      </tbody>
    </table>
  );
};

export default ParameterSetter;