import React from 'react';

const ParameterSetter = (prop) => {
  const display_params = {
    European: ["r", "t", "s", "sigma", "q", "k"],
    ImpliedVolatility: ["r", "t", "s", "q", "k", "option_price"],
    Asian: ["r", "t", "s", "sigma", "k", "mean_method", "n", "m", "is_control_variate", "use_simulation"],
    Basket: ["r", "t", "s", "sigma", "s2", "sigma2", "k", "mean_method", "m", "is_control_variate", "use_simulation"],
    American: ["r", "t", "s", "sigma", "k", "n"],
    KIKO: ["r", "t", "s", "sigma", "k", "n", "m", "barrier_low", "barrier_high", "rebate"],
  }
  const handleParameterChange = (event) => {
    const { name, value } = event.target;
    if (name === "mean_method") {
      if (prop.parameters["mean_method"] === "Arithmetic") {
        prop.setParameters((prevParameters) => ({
          ...prevParameters,
          use_simulation: true,
        }));
      }
      if (prop.parameters["mean_method"] === "Geometric") {
        prop.setParameters((prevParameters) => ({
          ...prevParameters,
          use_simulation: false,
        }));
      }
    }
    prop.setParameters((prevParameters) => ({
      ...prevParameters,
      [name]: isNaN(parseFloat(value)) ? value : parseFloat(value),
    }));
  };

  const show_parameters = display_params[prop.pricer]

  const create_option_type = (
    <tr>
      <td>option_type</td>
      <td>
        {["Call", "Put"].map((choice) => (
          <div key={choice}>
            <input
              type="radio"
              key={choice}
              name="option_type"
              value={choice}
              checked={choice === prop.parameters["option_type"]}
              onChange={handleParameterChange}
            />
            <label htmlFor={choice}>{choice}</label>
          </div>
        ))}
      </td>
    </tr>)

  return (
    <table>
      <tbody>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
      {create_option_type}
      {show_parameters.map(i => (
        <tr>
          <td>{i}</td>
          <td>
            <input
              type="text"
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