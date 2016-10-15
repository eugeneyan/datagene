class AddSeniorityToUsers < ActiveRecord::Migration
  def change
  	add_column :users, :seniority, :string
  end
end
