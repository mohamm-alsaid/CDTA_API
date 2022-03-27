CREATE TABLE [DTMs] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [anon_id] nvarchar(255),
  [mvot] int
)
GO

CREATE TABLE [MVoTs] (
  [mvot_id] int PRIMARY KEY,
  [registration_date] timestamp,
  [last_timestamp] timestamp,
  [ssdt] float,
  [RFC] float,
  [TSLC] float,
  [tx_time] float,
  [comm_freq] float,
  [certainty] float,
  [avg_tx_time] float,
  [trust_score] float,
  [distrust_score] float,
  [total_msgs] int,
  [other_count] int,
  [alerts_count] int,
  [timeout_count] int,
  [count_expected_msgs] int,
  [count_unexpected_msgs] int
)
GO

ALTER TABLE [DTMs] ADD FOREIGN KEY ([mvot]) REFERENCES [MVoTs] ([mvot_id])
GO
