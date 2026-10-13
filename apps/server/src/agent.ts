import "./config.ts";
import { HttpAgent } from "@ag-ui/client";
import {
  type AgentsFactory,
  type CopilotKitIntelligence,
  CopilotRuntime,
  createCopilotHonoHandler,
} from "@copilotkit/runtime/v2";
import type { Auth } from "./auth.ts";
import { brand } from "./brand.ts";
import type { Config } from "./config.ts";
import { ConversationAgent } from "./engine/conversation.ts";
import type { AgentService } from "./engine/service.ts";
import { createJevAdapter, type JevAdapter } from "./jev/adapter.ts";

export function agentConfigured(config: Config) {
  return (
    config.agentBackend === "sample" ||
    (config.agentBackend === "agui"
      ? Boolean(config.agentUrl)
      : Boolean(
          config.model &&
            (process.env.OPENAI_API_KEY ||
              process.env.ANTHROPIC_API_KEY ||
              process.env.GOOGLE_API_KEY),
        ))
  );
}
export function makeRuntime(
  config: Config,
  service: AgentService,
  auth: Auth,
  intelligence?: CopilotKitIntelligence,
) {
  // Built on first use, then shared so live mode reuses one TypeSafe client across requests.
  let jevAdapter: JevAdapter | undefined;
  const sharedJevAdapter = () => (jevAdapter ??= createJevAdapter(config));
  const agents: AgentsFactory = async ({ request }) => {
    if (config.agentBackend === "agui")
      return {
        default: new HttpAgent({
          url: config.agentUrl ?? "http://127.0.0.1:1/unconfigured",
          headers: config.agentToken ? { Authorization: `Bearer ${config.agentToken}` } : {},
        }),
      };
    const owner = await auth.owner(request.headers.get("authorization") ?? undefined);
    const memoryFile = await service.db
      .get<{ content: string }>(owner, "memory-file", "MEMORY.md")
      .catch(() => undefined);
    const memory = memoryFile?.content?.trim() ? memoryFile.content.trim() : undefined;
    return {
      default: new ConversationAgent(config, service, owner, sharedJevAdapter(), memory),
    };
  };
  // The shared CopilotKit sink carries this tag onto existing PostHog events.
  const telemetryProperties = { accessibility_title: brand.name };
  // Without an Intelligence key the runtime runs in SSE mode: chat and tools work,
  // but threads are not durable server-side (the app falls back to the local
  // conversation). identifyUser is an Intelligence-mode option only.
  const runtime = intelligence
    ? new CopilotRuntime({
        agents,
        intelligence,
        telemetryProperties,
        identifyUser: async (request) => ({
          id: await auth.owner(request.headers.get("authorization") ?? undefined),
          name: `${brand.name} user`,
        }),
        generateThreadNames: false,
      })
    : new CopilotRuntime({ agents, telemetryProperties });
  return createCopilotHonoHandler({ runtime, basePath: "/api/copilotkit" });
}
