import React, { useEffect, useState } from "react";
import axios from "axios";
import { CSVLink } from "react-csv";

function App() {

  const [incidents, setIncidents] = useState([]);

  const [search, setSearch] = useState("");

  const [form, setForm] = useState({
    incident_id: "",
    root_cause: "",
    fix_applied: "",
    prevention_steps: ""
  });

  const fetchIncidents = async () => {

    try {

      const response = await axios.get(
        "http://44.204.171.66:8000/incidents"
      );

      setIncidents(response.data);

    } catch (error) {

      console.log(error);

      alert("Backend Connection Failed");
    }
  };

  useEffect(() => {

    fetchIncidents();

    const interval = setInterval(() => {

      fetchIncidents();

    }, 5000);

    return () => clearInterval(interval);

  }, []);

  const submitRCA = async () => {

    try {

      await axios.post(
        "http://44.204.171.66:8000/rca",
        {
          incident_id: Number(form.incident_id),
          root_cause: form.root_cause,
          fix_applied: form.fix_applied,
          prevention_steps: form.prevention_steps
        }
      );

      alert("RCA Submitted");

      fetchIncidents();

    } catch (error) {

      console.log(error);

      alert("RCA Failed");
    }
  };

  const updateState = async (
    incidentId,
    state
  ) => {

    try {

      await axios.put(
        `http://44.204.171.66:8000/incidents/${incidentId}/state?state=${state}`
      );

      fetchIncidents();

    } catch (error) {

      console.log(error);

      alert("State Update Failed");
    }
  };

  const totalIncidents = incidents.length;

  const openIncidents = incidents.filter(
    (incident) => incident.state === "OPEN"
  ).length;

  const closedIncidents = incidents.filter(
    (incident) => incident.state === "CLOSED"
  ).length;

  const filteredIncidents = incidents.filter(
    (incident) =>
      incident.component_id
        .toLowerCase()
        .includes(search.toLowerCase())
  );

  return (

    <div style={{
      padding: "20px",
      backgroundColor: "#121212",
      minHeight: "100vh",
      color: "white"
    }}>

      <h1>IMS Dashboard</h1>

      <div style={{
        display: "flex",
        gap: "20px",
        marginBottom: "20px"
      }}>

        <div style={{
          border: "1px solid white",
          padding: "20px"
        }}>
          <h3>Total Incidents</h3>
          <h2>{totalIncidents}</h2>
        </div>

        <div style={{
          border: "1px solid white",
          padding: "20px"
        }}>
          <h3>Open Incidents</h3>
          <h2>{openIncidents}</h2>
        </div>

        <div style={{
          border: "1px solid white",
          padding: "20px"
        }}>
          <h3>Closed Incidents</h3>
          <h2>{closedIncidents}</h2>
        </div>

      </div>

      <input
        placeholder="Search Component"
        onChange={(e) =>
          setSearch(e.target.value)
        }
        style={{
          padding: "10px",
          width: "300px"
        }}
      />

      <br /><br />

      <button onClick={fetchIncidents}>
        Refresh
      </button>

      &nbsp;&nbsp;

      <CSVLink
        data={incidents}
        filename={"incidents.csv"}
      >
        <button>
          Export CSV
        </button>
      </CSVLink>

      <br /><br />

      <table
        border="1"
        cellPadding="10"
        style={{
          color: "white",
          borderColor: "white"
        }}
      >

        <thead>

          <tr>
            <th>ID</th>
            <th>Component</th>
            <th>Severity</th>
            <th>State</th>
            <th>MTTR</th>
            <th>Actions</th>
          </tr>

        </thead>

        <tbody>

          {filteredIncidents.map((incident) => (

            <tr key={incident.id}>

              <td>{incident.id}</td>

              <td>{incident.component_id}</td>

              <td style={{
                color:
                  incident.severity === "P0"
                    ? "red"
                    : incident.severity === "P1"
                    ? "orange"
                    : "lightgreen"
              }}>
                {incident.severity}
              </td>

              <td style={{
                color:
                  incident.state === "OPEN"
                    ? "red"
                    : incident.state === "INVESTIGATING"
                    ? "orange"
                    : incident.state === "RESOLVED"
                    ? "skyblue"
                    : "lightgreen"
              }}>
                {incident.state}
              </td>

              <td>{incident.mttr}</td>

              <td>

                <button
                  onClick={() =>
                    updateState(
                      incident.id,
                      "INVESTIGATING"
                    )
                  }
                >
                  Investigating
                </button>

                <br /><br />

                <button
                  onClick={() =>
                    updateState(
                      incident.id,
                      "RESOLVED"
                    )
                  }
                >
                  Resolved
                </button>

                <br /><br />

                <button
                  onClick={() =>
                    updateState(
                      incident.id,
                      "CLOSED"
                    )
                  }
                >
                  Close
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

      <br /><br />

      <h2>Submit RCA</h2>

      <input
        placeholder="Incident ID"
        onChange={(e) =>
          setForm({
            ...form,
            incident_id: e.target.value
          })
        }
      />

      <br /><br />

      <input
        placeholder="Root Cause"
        onChange={(e) =>
          setForm({
            ...form,
            root_cause: e.target.value
          })
        }
      />

      <br /><br />

      <input
        placeholder="Fix Applied"
        onChange={(e) =>
          setForm({
            ...form,
            fix_applied: e.target.value
          })
        }
      />

      <br /><br />

      <input
        placeholder="Prevention Steps"
        onChange={(e) =>
          setForm({
            ...form,
            prevention_steps: e.target.value
          })
        }
      />

      <br /><br />

      <button onClick={submitRCA}>
        Submit RCA
      </button>

    </div>
  );
}

export default App;
