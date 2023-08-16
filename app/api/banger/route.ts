import { Configuration, OpenAIApi } from "openai-edge";
// import { OpenAIStream, StreamingTextResponse } from "ai";

export const runtime = "edge";

const apiConfig = new Configuration({
  apiKey: process.env.OPENAI_API_KEY!,
});

const openai = new OpenAIApi(apiConfig);

// Build a prompt for the banger tweet
function buildPrompt(tweet: string) {
  return `Turn this tweet into a solid banger, where a banger is a tweet of shocking and mildly psychotic comedic value, that's prone to go viral: '${tweet}'`;
}

export async function POST(req: Request) {
  // Extract the `tweet` from the body of the request
  const { tweet } = await req.json();

  // Request the OpenAI API for the response based on the prompt
  const response = await openai.createCompletion({
    model: "text-davinci-003", //You can choose a different engine based on your subscription
    // stream: true,
    prompt: buildPrompt(tweet),
    max_tokens: 100,
    temperature: 0.7, //Adjust the temperature for more randomness (0.2 to 1.0)
    top_p: 1,
  });
  // Respond with the JSON
  const json = await response.json();

  let bangerTweet = json.choices[0].text;

  bangerTweet = bangerTweet.replace(/#\S+/g, ""); // Remove hashtags
  bangerTweet = bangerTweet.replace(/"/g, ""); // Remove double quotes as quotes within output are single quotes
  bangerTweet = bangerTweet.replace(/\.$/, "").trim(); // Remove dot at the end if it exists

  // Respond with the processed banger tweet
  return new Response(bangerTweet);

  //** Uncomment the following to stream the response instead of returning it as JSON. ie When you're ~sure it won't return any hashtags **//
  // Convert the response into a friendly text-stream
  // const stream = OpenAIStream(response);

  // Respond with the stream
  // return new StreamingTextResponse(stream);
}
