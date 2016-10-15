class AddUserPropertiesToUsers < ActiveRecord::Migration
  def change
  	add_column :users, :first_name, :string
  	add_column :users, :last_name, :string
  	add_column :users, :gender, :string
  	add_column :users, :birthday, :date
  	add_column :users, :education, :string
  	add_column :users, :job_role, :string
  	add_column :users, :function, :string
  	add_column :users, :industry, :string
  end
end
