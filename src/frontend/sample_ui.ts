/**
 * Sample frontend module used to demonstrate the project structure.
 *
 * It calls the sample API's `POST /users` endpoint. The types mirror the
 * Pydantic models in `src/api/sample_api.py` so the contract is explicit on
 * both sides. Composition over inheritance is preferred: `UserClient` is
 * constructed with a `fetch` implementation rather than subclassing a base.
 */

/** Mirrors the API's `CreateUserRequest` model. */
export interface CreateUserRequest {
  name: string;
  email: string;
}

/** Mirrors the API's `UserResponse` model. */
export interface UserResponse {
  id: number;
  name: string;
  email: string;
}

/** Minimal subset of the Fetch API we depend on (injected for testability). */
type FetchLike = (
  input: string,
  init?: { method?: string; headers?: Record<string, string>; body?: string },
) => Promise<{ ok: boolean; status: number; json: () => Promise<unknown> }>;

/**
 * Thin client for the sample user API.
 *
 * The HTTP transport is injected so tests can supply a fake `fetch` without
 * touching the network (mirrors the "mock external dependencies" testing rule).
 */
export class UserClient {
  constructor(
    private readonly baseUrl: string,
    private readonly fetchImpl: FetchLike = fetch as unknown as FetchLike,
  ) {}

  /**
   * Create a user via the API.
   *
   * @param request - The validated creation payload.
   * @returns The created user returned by the server.
   * @throws Error when the server responds with a non-2xx status.
   */
  async createUser(request: CreateUserRequest): Promise<UserResponse> {
    const response = await this.fetchImpl(`${this.baseUrl}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`createUser failed with status ${response.status}`);
    }

    return (await response.json()) as UserResponse;
  }
}
