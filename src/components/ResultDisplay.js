const ResultDisplay = prop => {
  if (prop.result.empty) {
    return <div></div>
  }
  const value = prop.result.price
  const ci = prop.result.confidence_interval
  return (
    <div>
      <h2>Result</h2>
      <table>
        <tbody>
        <tr>
          <td>Value</td>
          <td>{` ${value.toFixed(6)}`}</td>
        </tr>
        {ci ? <tr>
          <td>95% Confidence Interval</td>
          <td>{`[${ci[0].toFixed(6)}, ${ci[1].toFixed(6)}]`}</td>
        </tr> : null}
        </tbody>
      </table>
    </div>
  )
}

export default ResultDisplay