import { Injectable, OnModuleDestroy } from '@nestjs/common';
import { Pool, PoolClient, QueryResultRow } from 'pg';

@Injectable()
export class DatabaseService implements OnModuleDestroy {
  private readonly pool = new Pool({
    connectionString:
      process.env.DATABASE_URL ??
      'postgresql://rag_platform:local_only_change_me@localhost:55432/rag_platform',
    max: Number(process.env.DATABASE_POOL_MAX ?? 8),
    connectionTimeoutMillis: 5_000,
    idleTimeoutMillis: 30_000,
  });

  query<T extends QueryResultRow>(text: string, values: unknown[] = []) {
    return this.pool.query<T>(text, values);
  }

  async transaction<T>(work: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const result = await work(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async health(): Promise<boolean> {
    const result = await this.query<{ vector_enabled: boolean }>(
      "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname='vector') vector_enabled",
    );
    return result.rows[0]?.vector_enabled ?? false;
  }

  async onModuleDestroy(): Promise<void> {
    await this.pool.end();
  }
}
