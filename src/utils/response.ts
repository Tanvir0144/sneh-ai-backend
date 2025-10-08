export const okResponse = (message: string, data?: any) => ({
  ok: true,
  message,
  data,
});

export const errorResponse = (error: string) => ({
  ok: false,
  error,
});
