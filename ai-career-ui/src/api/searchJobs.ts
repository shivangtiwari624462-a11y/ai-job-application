export async function searchJobs(data: {
  job_title: string;
  location: string;
  experience: string;
  platform: string;
}) {
  const response = await fetch("http://127.0.0.1:8000/search-jobs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("API failed");
  }

  return response.json();
}
