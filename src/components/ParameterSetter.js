import React from 'react';

const ParameterSetter = (prop) => {
  const display_params = {
    European: ["r", "t", "s", "sigma", "q", "k"],
    ImpliedVolatility: ["r", "t", "s", "q", "k", "option_price"],
    Asian: ["r", "t", "s", "sigma", "k", "mean_method", "n", "m", "is_control_variate", "use_simulation"],
    Basket: ["r", "t", "s", "sigma", "s2", "sigma2", "rho", "k", "mean_method", "m", "is_control_variate", "use_simulation"],
    American: ["r", "t", "s", "sigma", "k", "n"],
    KIKO: ["r", "t", "s", "sigma", "k", "n", "m", "barrier_low", "barrier_high", "rebate"],
  }
  const show_parameters = display_params[prop.pricer]
  const bool_params = ["use_simulation", "is_control_variate"]
  const text_params = ["option_type", "mean_method"]
  const numeric_fields = show_parameters.filter(i => !bool_params.includes(i) && i !== "mean_method")
  const handleParameterChange = (event) => {
    const { name, value } = event.target;
    if (name === "mean_method") {
      if (prop.parameters["mean_method"] === "Arithmetic") {
        prop.setParameters((prevParameters) => ({
          ...prevParameters,
          is_control_variate: false,
        }));
      }
    }
    let new_value;
    if (bool_params.includes(name)) {
      new_value = value === "true"
    } else {
      if (text_params.includes(name)) {
        new_value = value
      } else {
        new_value = parseFloat(value)
      }
    }
    prop.setParameters((prevParameters) => ({
      ...prevParameters,
      [name]: new_value,
    }));
  };


  const create_choices = (name, values) => (
    <tr>
      <td>{name}</td>
      <td>
        {values.map((choice) => (
          <div key={String(choice)}>
            <input
              type="radio"
              key={String(choice)}
              name={String(name)}
              value={choice}
              checked={choice === prop.parameters[name]}
              onChange={handleParameterChange}
            />
            <label htmlFor={String(choice)}>{String(choice)}</label>
          </div>
        ))}
      </td>
    </tr>
  )

  return (
    <div>
      <h2>
        Set Parameters
      </h2>
      <table>
        <tbody>
        <tr>
          <th>Name</th>
          <th>Value</th>
        </tr>
        {create_choices("option_type", ["Call", "Put"])}
        {show_parameters.includes("mean_method") ? create_choices("mean_method", ["Arithmetic", "Geometric"]) : null}
        {numeric_fields.map(i => (
          <tr>
            <td>{i}</td>
            <td>
              <input
                type="number"
                name={i}
                key={i}
                value={prop.parameters[i]}
                onChange={handleParameterChange}
                min={0}
              />
            </td>
          </tr>
        ))}
        {show_parameters.includes("use_simulation") ? create_choices("use_simulation", [true, false]) : null}
        {
          prop.parameters["use_simulation"] &&
          prop.parameters["mean_method"] === "Arithmetic" &&
          show_parameters.includes("is_control_variate") ? create_choices("is_control_variate", [true, false]) : null}
        </tbody>
      </table>
    </div>
  );
};

export default ParameterSetter;