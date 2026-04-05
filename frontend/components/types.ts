export type Persona = {
  id: string;
  name: string;
  title: string;
  summary: string;
  accent: string;
};

export type ChatMessage = {
  role: 'user' | 'assistant' | 'system';
  content: string;
};
