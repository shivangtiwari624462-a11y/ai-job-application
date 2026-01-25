import { useState } from "react";
import { searchJobs } from "./api/searchJobs";

type Job = {
  title: string;
  company: string;
  location: string;
  platform: string;
};

function App() {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [experience, setExperience] = useState("");
  const [platform, setPlatform] = useState("linkedin");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearchJobs = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await searchJobs({
        job_title: jobTitle,
        location: location,
        experience: experience,
        platform: platform,
      });

      setJobs(data.jobs || []);
    } catch (err) {
      setError("Backend error. Check server.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI Career OS 🚀</h1>

      <input
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Experience"
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
      />
      <br /><br />

      <select
        value={platform}
        onChange={(e) => setPlatform(e.target.value)}
      >
        <option value="linkedin">LinkedIn</option>
      </select>
      <br /><br />

      <button onClick={handleSearchJobs}>
        {loading ? "Searching..." : "Search Jobs"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <hr />

      <h2>Jobs Found</h2>

      {jobs.map((job, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px",
          }}
        >
          <h3>{job.title}</h3>
          <p>{job.company}</p>
          <p>{job.location}</p>
          <small>{job.platform}</small>
        </div>
      ))}
    </div>
  );
}

export default App;
