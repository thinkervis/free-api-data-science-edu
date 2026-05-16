-- Run this in Supabase SQL Editor for shared dataset likes.
create table if not exists public.dataset_likes (
  dataset_id text primary key,
  likes integer not null default 0,
  updated_at timestamptz not null default now()
);

alter table public.dataset_likes enable row level security;

drop policy if exists "dataset likes are readable" on public.dataset_likes;
create policy "dataset likes are readable"
  on public.dataset_likes for select
  using (true);

-- Writes go through the security definer RPC below, so anonymous clients do not need direct insert/update policies.
create or replace function public.increment_dataset_like(p_dataset_id text)
returns public.dataset_likes
language plpgsql
security definer
set search_path = public
as $$
declare
  row public.dataset_likes;
begin
  insert into public.dataset_likes(dataset_id, likes, updated_at)
  values (p_dataset_id, 1, now())
  on conflict (dataset_id)
  do update set likes = public.dataset_likes.likes + 1, updated_at = now()
  returning * into row;
  return row;
end;
$$;

grant execute on function public.increment_dataset_like(text) to anon, authenticated;
