tests = FileList[ 'startertests/**/startertest*.py' ]
tests.each do |test|
    task test do
        sh "python3 #{test}"
    end
end

task :starter_tests => tests.to_a

task :pytest do
    sh "pytest examples/tests/test_*.py"
end

task :unittest do
    sh "python3 -m unittest examples/tests/test_*.py"
end

task :default => [ :starter_tests, :examples ]
