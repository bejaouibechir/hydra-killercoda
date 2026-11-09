# 4. Follow the second project

The producer's successful HTTP run records a project end. The consumer's `after_project` rule sees it and starts the second project. Inspect its history:

~~~bash
hdrctl trigger history after_producer --project /root/lab/project-triggers/consumer
~~~

Find a new successful run after your webhook call. The history belongs to the consumer project, while the HTTP event is recorded under the producer. Press **Check** to verify the new consumer run.
