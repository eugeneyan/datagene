# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20140405124747) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "axes", force: true do |t|
    t.string   "name"
    t.text     "description"
    t.integer  "value"
    t.boolean  "active"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer  "game_type"
  end

  create_table "countries", force: true do |t|
    t.string   "name"
    t.boolean  "active"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "feedbacks", force: true do |t|
    t.integer  "user_id"
    t.integer  "qn1"
    t.integer  "qn2"
    t.integer  "qn3"
    t.integer  "qn4"
    t.integer  "qn5"
    t.integer  "qn6"
    t.string   "qn7"
    t.text     "qn8"
    t.text     "qn9"
    t.text     "qn10"
    t.text     "qn11"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "functions", force: true do |t|
    t.string   "name"
    t.boolean  "active"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "games", force: true do |t|
    t.string   "version"
    t.text     "result"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer  "user_id"
    t.integer  "game_type"
  end

  add_index "games", ["user_id"], name: "index_games_on_user_id", using: :btree

  create_table "industries", force: true do |t|
    t.string   "name"
    t.boolean  "active"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "skills", force: true do |t|
    t.string   "name"
    t.text     "description"
    t.boolean  "active"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "users", force: true do |t|
    t.string   "email",                  default: "", null: false
    t.string   "encrypted_password",     default: "", null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,  null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string   "current_sign_in_ip"
    t.string   "last_sign_in_ip"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "first_name"
    t.string   "last_name"
    t.string   "gender"
    t.date     "birthday"
    t.string   "education"
    t.string   "job_role"
    t.string   "function"
    t.string   "industry"
    t.string   "role"
    t.integer  "birthday_day"
    t.integer  "birthday_month"
    t.integer  "birthday_year"
    t.string   "seniority"
    t.string   "country"
    t.string   "organization"
  end

  add_index "users", ["email"], name: "index_users_on_email", unique: true, using: :btree
  add_index "users", ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true, using: :btree

end
