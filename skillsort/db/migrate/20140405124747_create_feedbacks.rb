class CreateFeedbacks < ActiveRecord::Migration
  def change
    create_table :feedbacks do |t|
      t.integer :user_id
      t.integer :qn1
      t.integer :qn2
      t.integer :qn3
      t.integer :qn4
      t.integer :qn5
      t.integer :qn6
      t.string :qn7
      t.text :qn8
      t.text :qn9
      t.text :qn10
      t.text :qn11

      t.timestamps
    end
  end
end
