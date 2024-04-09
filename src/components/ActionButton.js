const ActionButton = prop => {
  const text = prop.parameters.use_simulation ? "Simulate" : "Calculate"
  if (prop.error) {
    return <button disabled>{text}</button>
  } else {
    return <button onClick={prop.calculateOptionPrice}>{text}</button>
  }
}

export default ActionButton;