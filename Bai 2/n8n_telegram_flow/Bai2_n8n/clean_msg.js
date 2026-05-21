let text = $json.output;

if (typeof text !== 'string') {
  text = JSON.stringify(text);
}

return [
  {
    json: {
      reply: text
    }
  }
];
