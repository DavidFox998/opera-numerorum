import { pgTable, serial, text, integer, boolean, timestamp, index } from "drizzle-orm/pg-core";

export const ledgerCheckpointRerollHistoryTable = pgTable(
  "ledger_checkpoint_reroll_history",
  {
    id: serial("id").primaryKey(),
    timestamp: timestamp("timestamp", { withTimezone: true }).notNull().defaultNow(),
    durationMs: integer("duration_ms").notNull(),
    exitCode: integer("exit_code").notNull(),
    ok: boolean("ok").notNull(),
    error: text("error"),
    refereeName: text("referee_name"),
    ip: text("ip"),
  },
  (table) => ({
    timestampIdx: index("ledger_checkpoint_reroll_history_timestamp_idx").on(table.timestamp),
  }),
);

export type LedgerCheckpointRerollHistoryRow =
  typeof ledgerCheckpointRerollHistoryTable.$inferSelect;
export type InsertLedgerCheckpointRerollHistory =
  typeof ledgerCheckpointRerollHistoryTable.$inferInsert;
