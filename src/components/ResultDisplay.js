const ResultDisplay = prop => {
  if (Object.keys(prop.result).length) {
    const value = prop.result.price
    const ci = prop.result.confidence_interval
    const delta = prop.result.delta

    return (
      <div>
        <h2>Result</h2>
        <table>
          <tbody>
          <tr>
            <td>Value</td>
            <td>{`${value.toFixed(6)}`}</td>
          </tr>
          {ci ? <tr>
            <td>95% Confidence Interval</td>
            <td>{`[${ci[0].toFixed(6)}, ${ci[1].toFixed(6)}]`}</td>
          </tr> : null}
          {delta ? <tr>
            <td>Delta</td>
            <td>{delta.toFixed(6)}</td>
          </tr> : null}
          </tbody>
        </table>
      </div>
    )
  }
  return <div></div>


}

export default ResultDisplay