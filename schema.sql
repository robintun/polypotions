create table
  public.cart_items (
    cart_id integer generated by default as identity,
    potion_id integer not null,
    quantity integer null,
    constraint cart_items_pkey primary key (cart_id, potion_id),
    constraint cart_items_cart_id_fkey foreign key (cart_id) references carts (cart_id) on update cascade on delete cascade,
    constraint cart_items_potion_id_fkey foreign key (potion_id) references potions (id) on update cascade on delete cascade
  ) tablespace pg_default;

create table
  public.carts (
    cart_id integer generated by default as identity,
    customer_name text null,
    constraint carts_pkey primary key (cart_id),
    constraint carts_cart_id_key unique (cart_id)
  ) tablespace pg_default;

create table
  public.global_inventory (
    created_at timestamp with time zone not null default now(),
    num_red_ml integer null,
    gold integer null,
    num_green_ml integer null,
    num_blue_ml integer null,
    id integer generated by default as identity,
    num_dark_ml integer null,
    constraint global_inventory_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.potions (
    id integer generated by default as identity,
    sku text null,
    price integer null,
    inventory integer null,
    potion_type integer[] null,
    constraint potions_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.gold_ledger (
    id integer generated by default as identity,
    created_at timestamp with time zone not null default now(),
    change_of_gold integer null,
    constraint gold_ledger_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.ml_ledger (
    id integer generated by default as identity,
    created_at timestamp with time zone not null default now(),
    red_ml_change integer null,
    green_ml_change integer null,
    blue_ml_change integer null,
    dark_ml_change integer null,
    constraint ml_ledger_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.potions_ledger (
    id integer generated by default as identity,
    created_at timestamp with time zone not null default now(),
    potion_id integer null,
    change_of_potion integer null,
    constraint potions_ledger_pkey primary key (id),
    constraint potions_ledger_potion_id_fkey foreign key (potion_id) references potions (id)
  ) tablespace pg_default;
