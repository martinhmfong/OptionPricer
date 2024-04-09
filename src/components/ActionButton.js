const ActionButton = prop => {
  const text = prop.parameters.use_simulation ? "Simulate" : "Calculate"
  return <button onClick={prop.calculateOptionPrice}>{text}</button>
}

export default ActionButton;